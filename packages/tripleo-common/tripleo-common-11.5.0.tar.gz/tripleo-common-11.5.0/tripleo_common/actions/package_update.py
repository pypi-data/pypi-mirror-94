# Copyright 2016 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import logging
import time

from heatclient.common import template_utils
from heatclient import exc as heat_exc
from mistral_lib import actions
from swiftclient import exceptions as swiftexceptions

from tripleo_common.actions import base
from tripleo_common.actions import templates
from tripleo_common import constants
from tripleo_common.utils import plan as plan_utils

LOG = logging.getLogger(__name__)


class UpdateStackAction(base.TripleOAction):

    def __init__(self, timeout, container=constants.DEFAULT_CONTAINER_NAME):
        super(UpdateStackAction, self).__init__()
        self.container = container
        self.timeout_mins = timeout

    def run(self, context):
        # get the stack. Error if doesn't exist
        heat = self.get_orchestration_client(context)
        try:
            stack = heat.stacks.get(self.container)
        except heat_exc.HTTPNotFound:
            msg = "Error retrieving stack: %s" % self.container
            LOG.exception(msg)
            return actions.Result(error=msg)

        swift = self.get_object_client(context)

        try:
            env = plan_utils.get_env(swift, self.container)
        except swiftexceptions.ClientException as err:
            err_msg = ("Error retrieving environment for plan %s: %s" % (
                self.container, err))
            LOG.exception(err_msg)
            return actions.Result(error=err_msg)

        update_env = {
            'parameter_defaults': {
                'DeployIdentifier': int(time.time()),
            },
        }

        noop_env = {
            'resource_registry': {
                'OS::TripleO::DeploymentSteps': 'OS::Heat::None',
            },
        }

        for output in stack.to_dict().get('outputs', {}):
            if output['output_key'] == 'RoleData':
                for role in output['output_value']:
                    role_env = {
                        "OS::TripleO::Tasks::%sPreConfig" % role:
                        'OS::Heat::None',
                        "OS::TripleO::Tasks::%sPostConfig" % role:
                        'OS::Heat::None',
                    }
                    noop_env['resource_registry'].update(role_env)
        update_env.update(noop_env)
        template_utils.deep_update(env, update_env)
        try:
            plan_utils.put_env(swift, env)
        except swiftexceptions.ClientException as err:
            err_msg = ("Error updating environment for plan %s: %s" % (
                self.container, err))
            LOG.exception(err_msg)
            return actions.Result(error=err_msg)

        # process all plan files and create or update a stack
        process_templates_action = templates.ProcessTemplatesAction(
            container=self.container
        )
        processed_data = process_templates_action.run(context)

        # If we receive a 'Result' instance it is because the parent action
        # had an error.
        if isinstance(processed_data, actions.Result):
            return processed_data

        stack_args = processed_data.copy()

        LOG.info("Performing Heat stack update")
        LOG.info('updating stack: %s', stack.stack_name)
        return heat.stacks.update(stack.id, **stack_args)
