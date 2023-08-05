
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


@plugin_pool.register_plugin
class BreadcrumbPlugin(CMSPluginBase):
    """
    CMS plugin allowing to add breadcrumb at any place.
    """

    name = _('Breadcrumb')
    render_template = 'cms_qe/breadcrumb/breadcrumb_tag.html'
    cache = False
