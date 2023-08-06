=============================================
Django eduNEXT ecommerce-extensions app.
=============================================
.. image:: https://circleci.com/gh/eduNEXT/ecommerce-extensions.svg?style=shield
    :target: https://circleci.com/gh/eduNEXT/ecommerce-extensions

.. image:: https://codecov.io/gh/eduNEXT/ecommerce-extensions/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/eduNEXT/ecommerce-extensions

This repository contains an external django application, which adds multiple funtionalities in order to extend the `ecommerce`_ behaviour and avoid changing the base code directly.

Installation
############

Install with pip::

    pip install django-oauth-toolkit

Add `ecommerce_extensions.apps.EcommerceExtensionsConfig` to your `INSTALLED_APPS`, if you want to use payment processors, and add `ecommerce_extensions.tenant.apps.TenantConfig`  to your `INSTALLED_APPS`, if you want to use TenantOptions.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'ecommerce_extensions.apps.EcommerceExtensionsConfig',
        'ecommerce_extensions.tenant.apps.TenantConfig',
    )

Usage
#####
1) Add model TenantOptions: This model allows to override settings by tenant and it can be found in <ecommerce-site>/admin/edunext/tenantoptions/ 

2) Add new payment processors.

Integrate payment processors.
=============================

The django application offers some integrations listed below:

- Payu payment processor.
- Fomopay payment processor.

In order to activate these processor some configuratios are required.

1) Add urls. File ecommerce/extensions/payment/urls.py

.. code-block:: python

    from ecommerce_extensions.urls import urlpatterns as url_extensions
    ...

    urlpatterns = [
        url('', include((url_extensions, 'ecommerce_extensions'))),
        ...
    ]

2) Add payment processors. File ecommerce/settings/_oscar.py

.. code-block:: python

    PAYMENT_PROCESSORS = (
        ...
        'ecommerce_extensions.payment.processors.payu.Payu',
        'ecommerce_extensions.payment.processors.fomopay.Fomopay',
    )

3) Add html buttons. File ecommerce/templates/oscar/basket/partials/hosted_checkout_basket.html

.. code-block:: html

    {% for processor in payment_processors %}
        <button data-track-type="click"
                data-track-event="edx.bi.ecommerce.basket.payment_selected"
                data-track-category="checkout"
                data-processor-name="{{ processor.NAME|lower }}"
                data-track-checkout-type="hosted"
                class="btn payment-button"
                id="{{ processor.NAME|lower }}">
            {% if processor.NAME == 'cybersource' %}
                {% trans "Checkout" as tmsg %}{{ tmsg | force_escape }}
            {% elif processor.NAME == 'paypal' %}
                {# Translators: Do NOT translate the name PayPal. #}
                {% trans "Checkout with PayPal" as tmsg %}{{ tmsg | force_escape }}
            {% elif processor.NAME == 'payu' %}
                {# Translators: Do NOT translate the name PayU. #}
                {% trans "Checkout with PayU" as tmsg %}{{ tmsg | force_escape }}
            {% elif processor.NAME == 'fomopay' %}
                {# Translators: Do NOT translate the name WeChat. #}
                {% trans "Checkout with WeChat" as tmsg %}{{ tmsg | force_escape }}
            {% endif %}
        </button>
    {% endfor %}


.. _ecommerce: https://github.com/edx/ecommerce/
