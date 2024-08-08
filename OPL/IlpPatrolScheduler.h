//
// Created by Ibrahim Sorkhoh on 2024-06-28.
//

#ifndef PATROLSCHEDULING_ILPPATROLSCHEDULER_H
#define PATROLSCHEDULING_ILPPATROLSCHEDULER_H

#include <ilconcert/iloexpression.h>
#include <ilconcert/ilomodel.h>
#include <ilcplex/ilocplex.h>
#include <vector>

using std::vector;

class IlpPatrolScheduler {
private:
    vector<vector<int>> adjMatrix_;
    vector<vector<double>> travelTime_; // Travel time between locations
    int depot_; // Index representing the Depot location
    int Tmax_; // Maximum time that a location should be re-visited
    vector<int> O_max_; // Maximum operation time for each vehicle (i.e., 480 minutes)
    vector<int> S_max_; // Operation time for each vehicle per shift (i.e., 120 minutes)
    vector<int> patrolTime_; // Location patrol time (i.e., 5 minutes for normal locations and 10 for priority ones)
    vector<int> restTime_; // Minimum rest time for each vehicle in the depot_
    int numberOfCars_;
    vector<double> carAvailability_;
    int maxCarVisits_;
    int maxLocSessions_;
    int numberOfLocations_;
    vector<double> taul_;
    vector<double> taulg_;
    vector<int> carsInitialLocations_;
    vector<double> carsBreakStartTime_;
    vector<double> carsBreakEndTime_;



public:
    void setTravelTime(const vector<vector<double>> &travelTime);

    void setDepot(int depot);

    void setRestTime(const vector<int> &restTime);

    void setMaxCarVisits(int maxCarVisits);

    void setMaxLocSessions(int maxLocSessions);

    void setNumberOfLocations(int numberOfLocations);

    void setTaul(const vector<double> &taul);

    void setTaulg(const vector<double> &taulg);

    void setCarsInitialLocations(const vector<int> &carsInitialLocations);

    void setCarsBreakStartTime(const vector<double> &carsBreakStartTime);

    void setCarsBreakEndTime(const vector<double> &carsBreakEndTime);

    void setNumberOfCars(int numberOfCars);

    void setCarAvailability(const vector<double> &carAvailability);

    void setAdjMatrix(const vector<vector<int>> &adjMatrix);

    void setDopot(int dopot);

    void setTMax(int tMax);

    void setOMax(const vector<int> &oMax);

    void setSMax(const vector<int> &sMax);

    void setPatrolTime(const vector<int> &patrolTime);

    void setResTime(const vector<int> &resTime);

    void run();
};


#endif //PATROLSCHEDULING_ILPPATROLSCHEDULER_H
