kuwtg: Keeping Up With the Giants
=================================

What?
----

List your unread Github notifications via Github's notification API.

Why?
----

There might exist such people* who may find it easier than skimming Github notifications via email or the website.

*For some definition of people

How?
----

Run kuwtg thusly:

    kuwtg

Put your access token in `~/.config/kuwtg/kuwtg.conf` thusly:

    [tokens]
    access-token = <your-access-token-here>

The access token must be permitted to access your notifications.

Use 'k' and 'j' to navigate up and down in the list view, 'l' to view the current notification, 'q' to quit. In the notification detail 'k' and 'j' for up and down scrolling, 'h' or 'q' to navigate back to the list.

Requires?
---------

Requests [http://www.python-requests.org/en/latest/]
