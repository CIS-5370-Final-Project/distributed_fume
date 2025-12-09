import os
import glob
import time
import globals as g
import helper_functions.print_verbosity as pv


class SyncManager:
    def __init__(self):
        self.last_sync_time = time.time()
        self.sync_interval = 5
        self.known_files = set()

        self.base_dir = g.SYNC_DIRECTORY
        self.my_dir = os.path.join(self.base_dir, g.INSTANCE_ID)
        self.net_dir = os.path.join(self.my_dir, "network_responses")
        self.con_dir = os.path.join(self.my_dir, "console_responses")
        self.crash_dir = os.path.join(self.my_dir, "crashes")

        for d in [self.net_dir, self.con_dir, self.crash_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

        g.CRASH_DIRECTORY = self.crash_dir

    def save_input(self, category, key, payload):
        target_dir = self.net_dir if category == "network" else self.con_dir

        filename = f"id_{int(time.time() * 1000)}_{abs(hash(key))}"
        filepath = os.path.join(target_dir, filename)

        try:
            with open(filepath, "w") as f:
                if type(payload) == bytearray:
                    p_hex = payload.hex()
                elif type(payload) == list:
                    p_str = "".join(
                        [p if isinstance(p, str) else p.toString() for p in payload]
                    )
                    p_hex = p_str
                else:
                    p_hex = str(payload)

                f.write(f"{str(key)}\n{p_hex}")

            self.known_files.add(filepath)

        except Exception as e:
            pv.print_error(f"Failed to sync input to disk: {e}")

    def sync(self):
        if time.time() - self.last_sync_time < self.sync_interval:
            return

        pv.verbose_print("[SYNC] Scanning for inputs from other instances...")

        search_pattern = os.path.join(self.base_dir, "*", "*", "*")
        found_files = glob.glob(search_pattern)

        new_count = 0

        for filepath in found_files:
            if filepath.startswith(self.my_dir) or filepath in self.known_files:
                continue

            self.known_files.add(filepath)

            parent_dir = os.path.basename(os.path.dirname(filepath))

            try:
                with open(filepath, "r") as f:
                    lines = f.readlines()
                    if len(lines) < 2:
                        continue

                    key = lines[0].strip()
                    payload_hex = lines[1].strip()

                    try:
                        payload_bytes = bytearray.fromhex(payload_hex)
                    except ValueError:
                        continue

                    if parent_dir == "network_responses":
                        if key not in g.network_response_log:
                            g.network_response_log[key] = payload_bytes
                            new_count += 1
                    elif parent_dir == "console_responses":
                        if key not in g.console_response_log:
                            g.console_response_log[key] = payload_bytes
                            new_count += 1

            except Exception as e:
                pv.debug_print(f"Error syncing file {filepath}: {e}")

        if new_count > 0:
            pv.normal_print(
                f"[SYNC] Imported {new_count} new inputs from neighbor instances."
            )

        self.last_sync_time = time.time()
