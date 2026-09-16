PROGRAM main
  VAR
    tank_level : INT AT %QW0 := 50;
    pump_command : BOOL AT %QX0.0 := FALSE;
    pump_running : BOOL AT %QX0.1 := FALSE;
    high_level_alarm : BOOL AT %QX0.2 := FALSE;
    one_second : TON;
  END_VAR

(* The timer produces one pulse each second. *)
  one_second(IN := NOT one_second.Q, PT := T#1s);

  (* A high-level alarm stays active until the operator turns the pump off
     and the level drops below the limit. *)
  IF tank_level >= 80 THEN
    high_level_alarm := TRUE;
  ELSIF NOT pump_command THEN
    high_level_alarm := FALSE;
  END_IF;

  pump_running := pump_command AND NOT high_level_alarm;

  IF one_second.Q THEN
    IF pump_running AND tank_level < 100 THEN
      tank_level := tank_level + 1;
    ELSIF NOT pump_running AND tank_level > 0 THEN
      tank_level := tank_level - 1;
    END_IF;
  END_IF;

END_PROGRAM