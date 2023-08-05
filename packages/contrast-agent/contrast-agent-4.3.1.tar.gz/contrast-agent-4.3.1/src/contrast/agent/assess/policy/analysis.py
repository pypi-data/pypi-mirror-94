# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.preshift import Preshift
from contrast.agent.assess.policy import propagation_policy
from contrast.agent.assess.policy import source_policy
from contrast.agent.assess.policy import trigger_policy
from contrast.agent.assess.utils import get_self_for_method
from contrast.agent.settings_state import SettingsState
from contrast.utils.decorators import fail_safely


@fail_safely("Failed to perform assess analysis.")
def analyze(context, patch_policy, result, args, kwargs):
    if skip_analysis(context):
        return

    with scope.contrast_scope():
        self_obj = get_self_for_method(patch_policy, args)
        preshift = Preshift(self_obj, args, kwargs)

        _analyze(patch_policy, preshift, self_obj, result, args, kwargs)


def skip_analysis(context):
    """
    Skip analysis if there is no context, scope, or configuration is False
    :param context: RequestContext
    :return:
    """
    if not context:
        return True
    if scope.in_contrast_scope():
        return True
    return not SettingsState().is_assess_enabled()


def _analyze(patch_policy, preshift, self_obj, ret, args, kwargs=None):
    if not patch_policy:
        return

    context = contrast.CS__CONTEXT_TRACKER.current()
    if context is None:
        return

    if patch_policy.trigger_nodes:
        # Each node may potentially correspond to a different rule
        for node in patch_policy.trigger_nodes:
            if not scope.in_trigger_scope():
                with scope.trigger_scope():
                    trigger_policy.apply(node.rule, [node], ret, args, kwargs)

    if patch_policy.source_nodes:
        source_policy.apply(patch_policy.source_nodes, self_obj, ret, args, kwargs)

    if not scope.in_propagation_scope():
        if patch_policy.propagator_nodes:
            with scope.propagation_scope():
                propagation_policy.apply(patch_policy.propagator_nodes, preshift, ret)
