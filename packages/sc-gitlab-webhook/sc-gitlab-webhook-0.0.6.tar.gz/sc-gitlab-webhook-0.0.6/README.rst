.. image:: https://badge.fury.io/py/sc-gitlab-webhook.svg
    :target: https://badge.fury.io/py/sc-gitlab-webhook
.. image:: https://img.shields.io/pypi/pyversions/sc-gitlab-webhook
    :alt: PyPI - Python Version

A simple Gitlab WebHook
========================================

This project provides a Gitlab web hook to receive Gitlab events and process these events.


Installation
------------

It is possible to install the tool with `pip`::

    pip install sc-gitlab-webhook

Configuration
-------------

You can copy `default.yml <https://github.com/Scott-Lau/sc-gitlab-webhook/blob/master/webhook/tests/sample_config/default.yml>`_ to `~/.sc-gitlab-webhook/production.yml`
to initialize the production configuration.

The default configuration file looks like this::

    dev:
      # whether this program is running is development mode
      dev_mode: False

    # flask server info
    server:
      # flask server IP
      ip: "localhost"
      # flask server port
      port: 8080

    # rocketmq configurations
    rocketmq:
      # name server ip
      name_server_ip: "localhost"
      # name server port
      name_server_port: 9876
      # group id
      group_id: "GITLAB_WEBHOOK_MSG"
      # message topic
      msg_topic: "GITLAB_WEBHOOK"
      # message keys
      msg_keys: "GITLAB"
      # message tags
      msg_tags: "GITLAB"


Dependencies
------------

* `sc-utilities <https://github.com/Scott-Lau/sc-utilities>`_ >= 0.0.1
* `sc-config <https://github.com/Scott-Lau/sc-config>`_ >= 0.0.2
* `flask <https://github.com/pallets/flask>`_ >= 1.1.2
* `rocketmq-client-python <https://github.com/apache/rocketmq-client-python>`_ >= 2.0.0

Changes
-------

Version 0.0.6
    * Fix bug: convert dict to json

Version 0.0.5
    * Use `sc-utilities <https://github.com/Scott-Lau/sc-utilities>`_ for logging

Version 0.0.4
    * Include sample config when packaging

Version 0.0.1
    * Initial version

License
-------

The script is released under the MIT License.  The MIT License is registered
with and approved by the Open Source Initiative [1]_.

.. [1] https://opensource.org/licenses/MIT
