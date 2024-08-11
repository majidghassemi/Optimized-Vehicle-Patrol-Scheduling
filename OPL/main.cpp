#include "IlpPatrolScheduler.h"

using namespace std;

int main() {
    const auto M = 10000;
    IlpPatrolScheduler scheduler;

    vector<vector<int>> adjMatrix = {{0, 1, 1, 1},
                                     {1, 0, 1, 1},
                                     {1, 1, 0, 1},
                                     {1, 1, 1, 0}};
    scheduler.setAdjMatrix(adjMatrix);

    vector<vector<double>> travelTime = {{0, 10, 10, 10},
                                         {10, 0, 10, 10},
                                         {10, 10, 0, 10},
                                         {10, 10, 10, 0}};
    scheduler.setTravelTime(travelTime);

    int depot = 2;
    scheduler.setDepot(depot);
    int T = 12 * 60;
    scheduler.setTMax(T);
    scheduler.setNumberOfCars(2);
    scheduler.setMaxCarVisits(12);
    scheduler.setMaxLocSessions(3);
    scheduler.setNumberOfLocations(4);
    scheduler.setTaul({10, 10, 0, 10}); // the time required to patrol a location every session
    scheduler.setTaulg({0, 0, 0, 0}); // the minimum gap between the sessions in each location
    scheduler.setCarsInitialLocations({0, 0});
    scheduler.setCarsBreakStartTime({50, 70});
    scheduler.setCarsBreakEndTime({60, 80});
    scheduler.setResTime({9, 9});
    scheduler.run();

    return 0;
}
