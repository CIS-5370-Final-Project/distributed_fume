from parsers.parse_initializer import ParseInitializer
import helper_functions.determine_protocol_version as hpv
import helper_functions.print_verbosity as pv
import globals as g


def handle_network_response(recv):
    if len(recv) == 0:
        return

    if g.protocol_version == 0:
        g.protocol_version = hpv.determine_protocol_version(recv.hex())

    index = 0
    while index < len(recv.hex()):
        try:
            parser = ParseInitializer(recv.hex()[index:], g.protocol_version)

            G_fields = str(parser.parser.G_fields)
            if G_fields not in g.network_response_log.keys():
                g.network_response_log[G_fields] = g.payload
                pv.normal_print("Found new network response (%d found)" % len(g.network_response_log.keys()))

                if g.sync_manager:
                    g.sync_manager.save_input("network", G_fields, g.payload)

            index += 2 * (parser.parser.remainingLengthToInteger()) + 2 + len(parser.parser.remaining_length)

        except ValueError:
            index += 2