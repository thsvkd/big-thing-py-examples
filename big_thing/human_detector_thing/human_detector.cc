#include "human_detector.h"

using namespace sopiot;
using namespace std;
using namespace cv;

vector<int> time_window_human(TIMEWINDOW_SIZE, -1);
vector<double> time_window_social_distance(TIMEWINDOW_SIZE, -1);

int human_not_exist_time_ = 0;
string image_file_ = "../test.jpg";

int ParseHumanNumber() {
  char buffer[1024 * 10];
  int human_count = 0;

  FILE* fp = fopen("../obj.json", "r");
  fread(buffer, 1024 * 10, 1, fp);
  fclose(fp);
  json_object* parsed_json = json_tokener_parse(buffer);
  json_object* obj = json_object_object_get(parsed_json, "obj");

  if (json_object_get_type(obj) != json_type_array) {
    printf("json_type_array error!\n");
    return -1;
  }

  for (int i = 0; i < json_object_array_length(obj); i++) {
    json_object* select_obj = json_object_array_get_idx(obj, i);
    select_obj = json_object_object_get(select_obj, "ClassID");
    int ClassID = json_object_get_int(select_obj);
    if (ClassID == 1) human_count++;
  }

  json_object_put(parsed_json);
  return human_count;
}

double CalculateDistance(vector<vector<double>> input) {
  double distance = .0;
  for (int i = 0; i < input.size() - 1; i++) {
    for (int j = i + 1; j < input.size(); j++) {
      distance = sqrt(pow(input[i][0] - input[j][0], 2) +
                      pow(input[i][1] - input[j][1], 2));
    }
  }

  return distance;
}

double ParseSocialDistance() {
  char buffer[1024 * 10];
  double distance;
  vector<vector<double>> nodes(0, vector<double>(0, 0));

  FILE* fp = fopen("../obj.json", "r");
  fread(buffer, 1024 * 10, 1, fp);
  fclose(fp);

  json_object* parsed_json = json_tokener_parse(buffer);
  json_object* obj = json_object_object_get(parsed_json, "obj");

  if (json_object_get_type(obj) != json_type_array) {
    printf("json_type_array error!\n");
    return -1.0;
  }

  for (int i = 0; i < json_object_array_length(obj); i++) {
    json_object* select_obj = json_object_array_get_idx(obj, i);
    json_object* ClassID_obj = json_object_object_get(select_obj, "ClassID");

    int ClassID = json_object_get_int(ClassID_obj);
    if (ClassID == 1) {
      json_object* Center_obj = json_object_object_get(select_obj, "Center");
      json_object* x_obj = json_object_array_get_idx(Center_obj, 0);
      json_object* y_obj = json_object_array_get_idx(Center_obj, 1);
      double x = json_object_get_double(x_obj);
      double y = json_object_get_double(y_obj);

      vector<double> tmp = {x, y};
      nodes.push_back(tmp);
    }
  }

  json_object_put(parsed_json);

  if (nodes.size() == 0) return 0;
  distance = CalculateDistance(nodes);
  return distance;
}

char* SenseImageFile() { return ReadBinaryFile(image_file_); }

int SenseHumanNumber() {
  int human_count = 0;
  human_count = ParseHumanNumber();
  if (human_count < 0)
    human_count = time_window_human[0];
  else if (human_count == 0)
    human_not_exist_time_++;
  else
    human_not_exist_time_ = 0;

  return TimeWindow(time_window_human, human_count, TIMEWINDOW_SIZE);
}

double SenseSocialDistance() {
  double distance;
  distance = ParseSocialDistance();
  if (distance < 0) distance = time_window_social_distance[0];

  return TimeWindow(time_window_social_distance, distance, TIMEWINDOW_SIZE);
}

int SenseHumanNotExistTime() { return human_not_exist_time_ / 4; }