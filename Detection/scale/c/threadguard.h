//
// Created by Abdul Qadeer on 7/31/17.
//

#ifndef SENSS_THREADGUARD_H
#define SENSS_THREADGUARD_H

#endif //SENSS_THREADGUARD_H

#include <thread>
using namespace std;

class ThreadGuard{

 private:
  thread &t_;
 public:
  explicit ThreadGuard(thread t) : t_(t){};
  ThreadGuard(ThreadGuard const&) = delete; // Delete copy constructor - to prevent dangerously copying thread objects
  ThreadGuard& operator=(ThreadGuard const&) = delete; // Delete copy assignment constructor
  ~ThreadGuard(){
    if(t_.joinable()){
      t_.join();
    }

  }

};