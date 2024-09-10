{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block html %}
This is an <strong>html</strong> message.
<br>
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyb-zj28cSKthUawEO-QFHFs7GUKPIO9uY_Z74xK6RIlQj6WfPNqhetaGwBJAvPsSkXAc&usqp=CAU">
{% endblock %}