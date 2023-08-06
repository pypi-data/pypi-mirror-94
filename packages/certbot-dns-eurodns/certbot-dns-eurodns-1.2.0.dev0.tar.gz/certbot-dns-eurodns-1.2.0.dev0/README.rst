certbot-dns-eurodns
======================

EuroDNS_ DNS Authenticator plugin for certbot_.

This plugin automates the process of completing a ``dns-01`` challenge by
creating, and subsequently removing, TXT records using the `EuroDNS API`_.

.. _eurodns: https://eurodns.com
.. _`EuroDNS API`: https://docapi.eurodns.com/
.. _certbot: https://certbot.eff.org/


Named Arguments
---------------

================================================================  =====================================
``--certbot-dns-eurodns:dns-eurodns-credentials``                 EuroDNS credentials_ INI file. **(required)**
``--certbot-dns-eurodns:dns-eurodns-propagation-seconds``         The number of seconds to wait for DNS to propagate before asking the ACME server to verify the DNS record(Default: 30)
================================================================  =====================================

Note that the seemingly redundant ``certbot-dns-eurodns:`` prefix is imposed by
certbot for external plugins.

If you are using certbot **1.7.0** or higher, it is possible to use the unprefixed arguments and configuration options in `credentials.ini`. See the second example below.

Installation
------------

.. code-block:: bash
   
   pip install certbot-dns-eurodns

Credentials
-----------

Use of this plugin requires a configuration file containing EuroDNS API
credentials.

See the `EuroDNS API`_ documentation for more information.

An example ``credentials.ini`` file:

.. code-block:: ini

   dns_eurodns_applicationId = myuser
   dns_eurodns_apiKey = mysecretpassword
   dns_eurodns_endpoint = https://rest-api.eurodns.com/user-api-gateway/proxy

The path to this file can be provided interactively or using the
``--certbot-dns-eurodns:dns-eurodns-credentials`` command-line argument. Certbot
records the path to this file for use during renewal, but does not store the
file's contents.

**CAUTION:** You should protect these API credentials as you would the
password to your EuroDNS user account. Users who can read this file can use these
credentials to issue arbitrary API calls on your behalf. Users who can cause
Certbot to run using these credentials can complete a ``dns-01`` challenge to
acquire new certificates or revoke existing certificates for associated
domains, even if those domains aren't being managed by this server.

If applicable, we suggest that you create API credentials for domains used by your
application, in order to reduce the potential impact of lost credentials.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).


Examples
--------

To acquire a single certificate for both ``example.com`` and
``www.example.com``, waiting 120 seconds for DNS propagation (the default):

.. code-block:: bash

   certbot certonly \
     --authenticator certbot-dns-eurodns:dns-eurodns \
     --certbot-dns-eurodns:dns-eurodns-credentials /etc/letsencrypt/eurodns.ini \
     --certbot-dns-eurodns:dns-eurodns-propagation-seconds 120 \
     -d example.com \
     -d www.example.com

If you are using certbot **1.7.0** (released on august 4, 2020) or higher, you can now call the plugin without the prefix:

.. code-block:: bash

   certbot certonly \
     --authenticator dns-eurodns \
     --dns-eurodns-credentials /etc/letsencrypt/eurodns.ini \
     --dns-eurodns-propagation-seconds 120 \
     -d example.com \
     -d www.example.com

In this second example, make sure you are also removing the prefixes in `/etc/letsencrypt/eurodns.ini`. Certbot will fail to discover your credentials otherwise.