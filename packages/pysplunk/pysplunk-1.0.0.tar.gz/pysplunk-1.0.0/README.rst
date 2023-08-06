Simple Splunk module for logging
================================

This is a package for internal use only. Use with Python 3.8+.


Usage
-----

On command line:

``$ pip install pysplunk``

Add this code to the entryfile:

.. code:: python

    from pysplunk import splunk
    splunk.configure_logger(
        index="index_name",
        token="splunk_token",
        version="1.0.0",
        env="production",
        level="DEBUG")

To log something:

.. code:: python

  splunk.loginfo(
      account=account_id,
      workflowtype="workflow_type",
      workflowinstance="workflow_instance",
      msg="message",
      customfields={"customField1": 3})
  
  splunk.logdebug(
      account=account_id,
      workflowtype="workflow_type",
      workflowinstance="workflow_instance",
      msg="message",
      customfields={"customField1": 3})
  
  splunk.logwarn(
      account=account_id,
      workflowtype="workflow_type",
      workflowinstance="workflow_instance",
      msg="message",
      customfields={"customField1": 1, "customField2": "2"})
  
  splunk.logerror(
      account=account_id,
      workflowtype="workflow_type",
      workflowinstance="workflow_instance",
      msg="message",
      customfields={"customField1": 1},
      evidencia="Exception traceback")


Definitions
-----------

* *account*: An integer representing the ID of the logged account.
* *workflowtype*: Some identification for the overall operation, example: "login".
* *workflowinstance*: Some identification for the specific part of the operation, examples "start_login", "login_error", "superuser_login", etc
* *msg*: A desciptive message of the log.
* *customfields*: Additional fields, examples: "operation_id", "user_id", "product_id", etc.
* *evidencia*: Some string evidence (can be multiline) to attach into the log. This is convenient to add exceptions or API responses.


Configuration
-------------

* ``AEROSPIKE_EVIDENCE_URL`` URL for aerospike
* ``AEROSPIKE_EVIDENCE_TTL`` TTL for aerospike evidence, default: 2592000 seconds
* ``AEROSPIKE_EVIDENCE_TIMEOUT`` Timetou for sending data to aerospike, default: 0.800 seconds
* ``SPLUNK_URL`` URL for splunk
* ``SPLUNK_LOG_FORMAT`` Splunk log format, default is set in splunk.py
* ``SPLUNK_LOG_HANDLER_NAME`` Handler for splunk log, default: Log


Requirements
------------

splunkfowarder is required for this package work.
