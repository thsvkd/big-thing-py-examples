#ifndef HUMAN_DETECTOR_H
#define HUMAN_DETECTOR_H

#include "camera_utils.h"
#include "window_utils.h"

#include "thing.h"

#define TIMEWINDOW_SIZE 5

using namespace sopiot;
using namespace std;
using namespace cv;

int ParseHumanNumber();
double ParseSocialDistance();
double CalculateDistance(vector<vector<double>> input);

char *SenseImageFile();
int SenseHumanNumber();
double SenseSocialDistance();
int SenseHumanNotExistTime();

#endif