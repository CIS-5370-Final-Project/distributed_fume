X1 = 0.5
X2 = 0.5
X3 = 1
b = 0.5
c = [1 / 15] * 15
d = [1 / 3, 1 / 3, 1 / 3, 1 / 8]

TARGET_ADDR = "127.0.0.1"
TARGET_PORT = 1883

CHOOSE_MUTATION = 0.5
PACKET_SELECTION_UNIFORM_DISTRIBUTION = 1
FUZZING_STATE_UNIFORM_DISTRIBUTION = 1

FUZZING_INTENSITY = 0.1
CONSTRUCTION_INTENSITY = 3

START_COMMAND = ""
TARGET_START_TIME = 0.5

user_supplied_X = [0, 0, 0]

VERBOSITY = 1

payload = []

protocol_version = 0

network_response_log = {}
console_response_log = {}

SIMILARITY_THRESHOLD = 0.3

request_queue = []
REQUEST_QUEUE_SIZE = 5

TRIAGE_FAST = 1
TRIAGE_MAX_DEPTH = 3

CRASH_DIRECTORY = "crashes"
CRASH_FILENAME_PREFIX = "target"

MAXIMUM_PAYLOAD_LENGTH = 10000

SYNC_DIRECTORY = "fume_sync"
INSTANCE_ID = "default"
IS_MASTER = True
sync_manager = None

local_response_count = 0

# Run duration in minutes (0 = unlimited)
RUN_DURATION = 0
