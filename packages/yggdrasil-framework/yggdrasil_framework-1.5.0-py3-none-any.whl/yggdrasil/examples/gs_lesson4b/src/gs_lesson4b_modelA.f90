PROGRAM main
  ! Include methods for input/output channels
  USE fygg

  ! Declare resulting variables and create buffer for received message
  logical :: flag = .true.
  integer :: bufsiz
  character(len = 1000) :: buf
  TYPE(yggcomm) :: in_channel, out_channel

  ! Initialize input/output channels
  in_channel = ygg_input("inputA")
  out_channel = ygg_output("outputA")

  ! Loop until there is no longer input or the queues are closed
  DO WHILE (flag)
  
     ! Receive input from input channel
     ! If there is an error, the flag will be negative
     ! Otherwise, it is the size of the received message
     bufsiz = len(buf)
     flag = ygg_recv(in_channel, buf, bufsiz)
     IF (.not.flag) THEN
        PRINT *, "Model A: No more input."
        EXIT
     END IF

     ! Print received message
     PRINT *, "Model A: ", buf

     ! Send output to output channel
     ! If there is an error, the flag will be negative
     flag = ygg_send(out_channel, buf, bufsiz)
     IF (.not.flag) THEN
        PRINT *, "Model A: Error sending output."
        EXIT
     END IF

  END DO

END PROGRAM main
