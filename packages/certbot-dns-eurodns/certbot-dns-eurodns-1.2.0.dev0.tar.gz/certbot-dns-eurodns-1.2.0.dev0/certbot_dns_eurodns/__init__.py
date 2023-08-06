"""
The `~certbot_dns_eurodns.dns_eurodns` plugin automates the process of
completing a ``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and
subsequently removing, TXT records using the EuroDNS REST API.


Named Arguments
---------------

========================================  =====================================
``--dns-eurodns-credentials``           EuroDNS Remote API credentials_
                                          INI file. (Required)
``--dns-eurodns-propagation-seconds``   The number of seconds to wait for DNS
                                          to propagate before asking the ACME
                                          server to verify the DNS record.
                                          (Default: 30)
========================================  =====================================


Credentials
-----------

Use of this plugin requires a configuration file containing EuroDNS Remote API
credentials, obtained from your EuroDNS
`System > Remote Users`.

.. code-block:: ini
   :name: credentials.ini
   :caption: Example credentials file:

   # ISPCONFIG API credentials used by Certbot
   dns_eurodns_applicationId = myuser
   dns_eurodns_apiKey = mysecretpassword
   dns_eurodns_endpoint = https://rest-api.eurodns.com/user-api-gateway/proxy

The path to this file can be provided interactively or using the
``--dns-eurodns-credentials`` command-line argument. Certbot records the path
to this file for use during renewal, but does not store the file's contents.

.. caution::
   You should protect these API credentials as you would a password. Users who
   can read this file can use these credentials to issue arbitrary API calls on
   your behalf. Users who can cause Certbot to run using these credentials can
   complete a ``dns-01`` challenge to acquire new certificates or revoke
   existing certificates for associated domains, even if those domains aren't
   being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).

Examples
--------

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com``

   certbot certonly \\
     --dns-eurodns \\
     --dns-eurodns-credentials ~/.secrets/certbot/eurodns.ini \\
     -d example.com

.. code-block:: bash
   :caption: To acquire a single certificate for both ``example.com`` and
             ``www.example.com``

   certbot certonly \\
     --dns-eurodns \\
     --dns-eurodns-credentials ~/.secrets/certbot/eurodns.ini \\
     -d example.com \\
     -d www.example.com

.. code-block:: bash
   :caption: To acquire a certificate for ``example.com``, waiting 240 seconds
             for DNS propagation

   certbot certonly \\
     --dns-eurodns \\
     --dns-eurodns-credentials ~/.secrets/certbot/eurodns.ini \\
     --dns-eurodns-propagation-seconds 240 \\
     -d example.com

"""
