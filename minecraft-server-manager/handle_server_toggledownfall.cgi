#!/usr/bin/perl
# handle_server_logroll.cgi
# Rolls the logs for the server

require 'msm-lib.pl';
&ReadParse();

# Get the server input, and make sure it's valid.
my $server = $in{'name'};
if (!(grep { $_ eq $server } msm_server_list())) {
    error("No server with name: $server");
}

$err = &msm_server_toggledownfall($server);
&webmin_log("server toggledownfall");
&redirect("server.cgi?name=$server");
