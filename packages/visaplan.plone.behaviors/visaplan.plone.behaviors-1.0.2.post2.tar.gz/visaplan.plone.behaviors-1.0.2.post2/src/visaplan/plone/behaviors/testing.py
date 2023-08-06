# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import visaplan.plone.behaviors


class VisaplanPloneBehaviorsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=visaplan.plone.behaviors)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'visaplan.plone.behaviors:default')


VISAPLAN_PLONE_BEHAVIORS_FIXTURE = VisaplanPloneBehaviorsLayer()


VISAPLAN_PLONE_BEHAVIORS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VISAPLAN_PLONE_BEHAVIORS_FIXTURE,),
    name='VisaplanPloneBehaviorsLayer:IntegrationTesting',
)


VISAPLAN_PLONE_BEHAVIORS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VISAPLAN_PLONE_BEHAVIORS_FIXTURE,),
    name='VisaplanPloneBehaviorsLayer:FunctionalTesting',
)


VISAPLAN_PLONE_BEHAVIORS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        VISAPLAN_PLONE_BEHAVIORS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='VisaplanPloneBehaviorsLayer:AcceptanceTesting',
)
