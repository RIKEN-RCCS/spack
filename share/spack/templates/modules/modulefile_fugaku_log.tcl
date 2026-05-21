{% extends "modules/modulefile.tcl" %}

{% block footer %}
{{ super() }}

# Fugaku OSS usage logging
if {[module-info mode load]} {
  catch {
    system /vol0004/apps/oss/spack-v1.0.1/share/spack/templates/modules/mod_log.sh [module-info name]
  }
}
{% endblock %}
