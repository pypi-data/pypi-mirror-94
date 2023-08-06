#include <stdio.h>
// Include methods for input/output channels
#include "YggInterface.h"

int main(int argc, char *argv[]) {
  // Initialize input/output channels
  yggInput_t in_channel = yggJSONObjectInput("inputB");
  yggOutput_t out_channel = yggJSONObjectOutput("outputB");

  // Declare resulting variables and create buffer for received message
  int flag = 1;
  json_object_t obj = init_json_object();

  // Loop until there is no longer input or the queues are closed
  while (flag >= 0) {
  
    // Receive input from input channel
    // If there is an error, the flag will be negative
    // Otherwise, it is the size of the received message
    flag = yggRecv(in_channel, &obj);
    if (flag < 0) {
      printf("Model B: No more input.\n");
      break;
    }

    // Print received message
    printf("Model B:\n");
    display_json_object(obj);

    // Send output to output channel
    // If there is an error, the flag will be negative
    flag = yggSend(out_channel, obj);
    if (flag < 0) {
      printf("Model B: Error sending output.\n");
      break;
    }

  }

  // Free dynamically allocated obj structure
  free_json_object(&obj);
  
  return 0;
}

