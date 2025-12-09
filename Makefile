build_mosquitto:
	docker build -f Dockerfile.mosquitto -t mosquitto-2.0.7 .

run_mosquitto:
	docker run -it --rm -p 1883:1883 mosquitto-2.0.7