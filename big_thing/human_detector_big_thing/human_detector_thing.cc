#include "human_detector.h"

DEFINE_INTERRUPT_HANDLER

using namespace sopiot;
using namespace std;
using namespace cv;

// VideoCapture* cap_;
void* cap_;

Thing thing("HumanDetecter", "192.168.50.181", 1883, 60);

Value image_file("image_file", SenseHumanNotExistTime, 0, 1000000, 1000);
Value human_num("human_num", SenseHumanNumber, 0, 100, 1000);
Value social_distance("social_distance", SenseSocialDistance, 0, 10000, 1000);
Value no_human_time("no_human_time", SenseHumanNotExistTime, 0, 10000, 1000);

// void ActuateTakePhoto() { TakePhoto(cap_, image_file_); }

void Setup(int argc, char* argv[]) {
  SET_INTERRUPT_HANDLER

  thing.Add(image_file);
  thing.Add(human_num);
  thing.Add(social_distance);
  thing.Add(no_human_time);

  // thing->Add(ActuateTakePhoto);

  thing.Setup();
}

void Run() {
  while (doLoop) {
    thing.Publish();
    CAPTime_Sleep(100);
  }

  thing.Disconnect();
  SOPLOG("Thing end\n");
}

int main(int argc, char* argv[]) {
  Setup(argc, argv);
  Run();

  return 0;
}
