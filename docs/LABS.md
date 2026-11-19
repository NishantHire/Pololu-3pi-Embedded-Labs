# Lab catalog

Groups describe subject matter; they do not claim a particular course lab-number mapping.

## Timers and reusable reactors

| Program | Behavior |
| --- | --- |
| [ToolsBlinkSolution](../src/ToolsBlinkSolution.lf) | Two timers offset by 250 ms alternate GPIO writes |
| [ToolsPrintfSolution](../src/ToolsPrintfSolution.lf) | Adds serial ON/OFF messages |
| [ToolsLEDSolution](../src/ToolsLEDSolution.lf) | Uses the reusable [LED reactor](../src/lib/LED.lf) |

## Peripherals

| Program | Behavior |
| --- | --- |
| [PeripheralsDirectSolution](../src/PeripheralsDirectSolution.lf) | Writes RP2040 SIO GPIO set/clear registers |
| [PeripheralsButtonSolution](../src/PeripheralsButtonSolution.lf) | Reads the GPIO input register and displays active-low button state |

Verify pin polarity and board-specific behavior on the physical robot.

## Interrupts

| Program | Behavior |
| --- | --- |
| [InterruptCallbackSolution](../src/InterruptCallbackSolution.lf) | Prints GPIO and edge flags in a callback; a comparison exercise, not a recommended location for lengthy processing |
| [InterruptActionSolution](../src/InterruptActionSolution.lf) | Schedules a physical LF action from the callback and reports event intervals |
| [InterruptDebouncedSolution](../src/InterruptDebouncedSolution.lf) | Filters events using a 200 ms physical-time interval before scheduling an action |
| [InterruptModalSolution](../src/InterruptModalSolution.lf) | Switches between counting up every 500 ms and down every second on button events |

## Sensor processing

[SensorsTiltSolution](../src/SensorsTiltSolution.lf) samples the accelerometer every 250 ms and displays pitch and roll. The local [Tilt reactor](../src/lib/Tilt.lf) uses `atan2f` and the magnitude of the other two axes.

This is an accelerometer-based estimate, not a fused attitude estimator; acceleration during movement can affect it.

## Robot motion

| Program | Behavior |
| --- | --- |
| [RobotDriveSolution](../src/RobotDriveSolution.lf) | Alternates drive/stop commands using modes |
| [RobotEncoderSolution](../src/RobotEncoderSolution.lf) | Converts encoder angles to distance with a 31.75 mm wheel diameter |
| [RobotSquareSolution](../src/RobotSquareSolution.lf) | Alternates 0.5 m segments and nominal 90-degree turns; continues cycling rather than stopping after four sides |
| [RobotAvoidSolution](../src/RobotAvoidSolution.lf) | Adds bump-triggered 0.10 m reverse travel and nominal 45-degree avoidance turns |

These constants are setpoints, not measurements of achieved accuracy.

## Hill climbing

| Program | Behavior |
| --- | --- |
| [HillLineDetectSolution](../src/HillLineDetectSolution.lf) | Timed line calibration and edge-sensor display |
| [HillLineAvoidSolution](../src/HillLineAvoidSolution.lf) | Timed backing/turning recovery at dark edges |
| [HillClimbSolution](../src/HillClimbSolution.lf) | Combines line detection, encoders, tilt, gyroscope, and feedback-controlled wheel speeds |

The integrated controller has ten modes: `CALIBRATING`, `CLIMBING`, `BACKING_UP`, `TURNING_UP`, `TOP_PAUSE`, `TURNING_AROUND`, `DESCENDING`, `BACKING_DOWN`, `TURNING_DOWN`, and `STOPPED`.

### Current tuning

- Sensor sampling: 50 ms; line calibration: 10 seconds.
- Dark threshold: 500; slope threshold: 7 degrees; level threshold: 4 degrees.
- Level detection: 20 qualifying samples, approximately one second at the configured sample period.
- Requested climb/descent speeds: 0.10/0.08 m/s. These are controller setpoints.
- Roll gain: 0.0005; correction is clamped to +/-0.01.
- Backing: 500 ms; edge-recovery turn: 650 ms; top pause: 500 ms.
- Turnaround threshold: **160 degrees**, although the display says `TURNING 180`. This is a tuning parameter, not proof of an exact measured 180-degree turn.
- Both motor-trim constants are currently zero.

Motion can begin automatically after calibration. Use a controlled test surface and a way to stop and catch the robot.
