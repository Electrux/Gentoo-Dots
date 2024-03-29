#!/bin/bash

USER_NAME=$(who | awk -v vt=tty$(fgconsole) '$0 ~ vt {print $1}' | tail -1)
USER_ID=$(id -u "$USER_NAME")
CARD_PATH="/sys/class/drm/card0/"
AUDIO_OUTPUT="analog-surround-40"
PULSE_SERVER="unix:/run/user/"$USER_ID"/pulse/native"

for OUTPUT in $(cd "$CARD_PATH" && echo card*); do
  OUT_STATUS=$(<"$CARD_PATH"/"$OUTPUT"/status)
  if [[ $OUT_STATUS == connected ]]
  then
    echo $OUTPUT connected
    case "$OUTPUT" in
      "card0-HDMI-A-1")
        AUDIO_OUTPUT="hdmi-stereo" # Digital Stereo (HDMI 1)
	DEFAULT_SINK="alsa_output.pci-0000_00_03.0.hdmi-stereo"
     ;;
      "card0-HDMI-A-2")
        AUDIO_OUTPUT="hdmi-stereo-extra1" # Digital Stereo (HDMI 2)
	DEFAULT_SINK="alsa_output.pci-0000_00_03.0.hdmi-stereo-extra1"
     ;;
      "card0-HDMI-A-3")
        AUDIO_OUTPUT="hdmi-stereo-extra2" # Digital Stereo (HDMI 3)
	DEFAULT_SINK="alsa_output.pci-0000_00_03.0.hdmi-stereo-extra2"
     ;;
     "card0-eDP-1")
	AUDIO_OUTPUT="analog-stereo" # Default speakers
	DEFAULT_SINK="alsa_output.pci-0000_00_1b.0.analog-stereo"
     ;;
    esac
  fi
done
echo selecting output $AUDIO_OUTPUT
sudo -u "$USER_NAME" pactl --server "$PULSE_SERVER" set-card-profile 0 output:"$AUDIO_OUTPUT"
sudo -u "$USER_NAME" pactl --server "$PULSE_SERVER" set-default-sink "$DEFAULT_SINK"
