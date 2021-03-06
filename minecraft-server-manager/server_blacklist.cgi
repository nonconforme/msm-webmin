#!/usr/bin/perl
# server_blacklist.cgi
# Modify the users on the blacklist

require 'msm-lib.pl';
&ReadParse();
my $server = $in{'name'};

&ui_print_header(undef, "Blacklist Management: \"$server\"", "", "options");

print "
<div class=\"alert alert-warning\">
<strong>Warning</strong>
<div>Some features on this page may be broken or incomplete. If you have problems, please check the <a href=\"https://github.com/bplower/msm-webmin\">open bug reports</a>.</div>
</div>
";

# Whitelist on/off buttons
my @players = msm_server_connected($server);
my @blacklist = msm_server_blacklist_list($server);
my @unblacklisted = ();

# This is really not performant, but it's the quickest way to get the complement
# between @players and @blacklist.
# TODO: Make this more efficient
foreach my $i (@players) {
    if (!(grep { $_ eq $i } @blacklist)) {
        push(@unblacklisted, $i);
    }
}

$blacklist_len = @blacklist;
print "<h3> Blacklisted Users </h3>";
if ($blacklist_len == 0) {
    print "<strong>The blacklist is empty.</strong>";
}
else {
    print ui_columns_start(["Player Name", "Remove from the blacklist"], undef, "noborder", undef, undef);
    foreach (@blacklist) {
        $remove = ui_buttons_row("handle_server_player_blacklist.cgi?server=$server&player=$_&action=remove", "Remove", "");
        print ui_columns_row([html_escape($_), $remove]);
    }
    print ui_columns_end();
}

print "<h3> Normal Users </h3>";
&ui_form_columns_table("handle_server_blacklist_players.cgi",   # cgi
                       [ [ undef, $text{'save'} ] ],            # &buttons
                       1,                                       # select-all
                       undef,                                   # &otherlinks
                       [["name", $server]],                     # &hiddens
                       [],                                      # &headings
                       100,                                     # width-percent
                       [],                                      # &data
                       undef,                                   # &types
                       1,                                       # no-sort
                       "butts",                                 # title
                       "this is empty"                          # empty-msg
                       );
ui_checked_columns_row(["testing"]);
foreach (@players) {
    ui_columns_row([$_]);
}
&ui_form_end();



# print &ui_form_start("handle_server_whitelist_players.cgi");
# print &ui_table_start("Whitelist Players", "width=100%", 2);

# print &ui_table_row("Player(s)", &ui_select("player", "", \@unblacklisted, 15, 1));
# print &ui_hidden("action", "create");

# print &ui_table_end();
# print &ui_form_end([ [ undef, $text{'save'} ] ]);

# print &ui_form_start("handle_server_name.cgi");
# print &ui_table_start("Un-Whitelist Players", "width=100%", 2);

# print &ui_table_row("Player(s)", &ui_select("player", "", \@blacklist, 15, 1));
# print &ui_hidden("action", "create");

# print &ui_table_end();
# print &ui_form_end([ [ undef, $text{'save'} ] ]);

&ui_print_footer("server.cgi?name=$server", "server");
