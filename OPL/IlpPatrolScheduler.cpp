//
// Created by Ibrahim Sorkhoh on 2024-06-28.
//

#include "IlpPatrolScheduler.h"
#include <iostream>

using std::cout;
using std::endl;
using std::string;
using std::to_string;

typedef IloArray<IloArray<IloArray<IloIntVarArray>>> FourDimIntArray;
typedef IloArray<IloArray<IloIntVarArray>> ThreeDimIntArray;
typedef IloArray<IloIntVarArray> TwoDimIntArray;
typedef IloIntVarArray OneDimIntArray;

typedef IloArray<IloArray<IloArray<IloNumVarArray>>> FourDimNumArray;
typedef IloArray<IloArray<IloNumVarArray>> ThreeDimNumArray;
typedef IloArray<IloNumVarArray> TwoDimNumArray;
typedef IloNumVarArray OneDimNumArray;

FourDimIntArray
initFourDimIntVarArray(IloEnv &env, int dim1, int dim2, int dim3, int dim4, int min, int max, const string &name,
                       const vector<string> &indexes) {
    FourDimIntArray result(env, dim1);
    for (int i = 0; i < result.getSize(); ++i) {
        result[i] = ThreeDimIntArray(env, dim2);
        for (int j = 0; j < result[i].getSize(); ++j) {
            result[i][j] = TwoDimIntArray(env, dim3);
            for (int k = 0; k < result[i][j].getSize(); ++k) {
                result[i][j][k] = OneDimIntArray(env, dim4, min, max);
                string variableName = name
                                      + "_" + indexes[0] + to_string(i)
                                      + "_" + indexes[1] + to_string(j)
                                      + "_" + indexes[2] + to_string(k)
                                      + "_" + indexes[3];
                result[i][j][k].setNames(variableName.c_str());

            }
        }
    }

    return result;
}

FourDimNumArray
initFourDimNumVarArray(IloEnv &env, int dim1, int dim2, int dim3, int dim4, int min, int max, const string &name,
                       const vector<string> &indexes) {
    FourDimNumArray result(env, dim1);
    for (int i = 0; i < result.getSize(); ++i) {
        result[i] = ThreeDimNumArray(env, dim2);
        for (int j = 0; j < result[i].getSize(); ++j) {
            result[i][j] = TwoDimNumArray(env, dim3);
            for (int k = 0; k < result[i][j][k].getSize(); ++k) {
                result[i][j][k] = OneDimNumArray(env, dim4, min, max);
                string variableName = name
                                      + "_" + indexes[0] + to_string(i)
                                      + "_" + indexes[1] + to_string(j)
                                      + "_" + indexes[2] + to_string(k)
                                      + "_" + indexes[3];
                result[i][j][k].setNames(variableName.c_str());
            }
        }
    }

    return result;
}

ThreeDimIntArray
initThreeDimIntVarArray(IloEnv &env, int dim2, int dim3, int dim4, int min, int max, const string &name,
                        const vector<string> &indexes) {

    ThreeDimIntArray result = ThreeDimIntArray(env, dim2);
    for (int j = 0; j < result.getSize(); ++j) {
        result[j] = TwoDimIntArray(env, dim3);
        for (int k = 0; k < result[j].getSize(); ++k) {
            result[j][k] = OneDimIntArray(env, dim4, min, max);
            string variableName = name
                                  + "_" + indexes[0] + to_string(j)
                                  + "_" + indexes[1] + to_string(k)
                                  + "_" + indexes[2];
            result[j][k].setNames(variableName.c_str());
        }
    }

    return result;
}

ThreeDimNumArray
initThreeDimNumVarArray(IloEnv &env, int dim2, int dim3, int dim4, int min, int max, const string &name,
                        const vector<string> &indexes) {

    ThreeDimNumArray result = ThreeDimNumArray(env, dim2);
    for (int j = 0; j < result.getSize(); ++j) {
        result[j] = TwoDimNumArray(env, dim3);
        for (int k = 0; k < result[j][k].getSize(); ++k) {
            result[j][k] = OneDimNumArray(env, dim4, min, max);
            string variableName = name
                                  + "_" + indexes[0] + to_string(j)
                                  + "_" + indexes[1] + to_string(k)
                                  + "_" + indexes[2];
            result[j][k].setNames(variableName.c_str());
        }
    }

    return result;
}

TwoDimIntArray initTwoDimIntVarArray(IloEnv &env, int dim3, int dim4, int min, int max, const string &name,
                                     const vector<string> &indexes) {

    TwoDimIntArray result = TwoDimIntArray(env, dim3);
    for (int k = 0; k < result[k].getSize(); ++k) {
        result[k] = OneDimIntArray(env, dim4, min, max);
        string variableName = name
                              + "_" + indexes[0] + to_string(k)
                              + "_" + indexes[1];
        result[k].setNames(variableName.c_str());
    }

    return result;
}

TwoDimNumArray initTwoDimNumVarArray(IloEnv &env, int dim3, int dim4, int min, int max, const string &name,
                                     const vector<string> &indexes) {

    TwoDimNumArray result = TwoDimNumArray(env, dim3);
    for (int k = 0; k < result.getSize(); ++k) {
        result[k] = OneDimNumArray(env, dim4, min, max);
        string variableName = name
                              + "_" + indexes[0] + to_string(k)
                              + "_" + indexes[1];
        result[k].setNames(variableName.c_str());
    }

    return result;
}

OneDimIntArray initOneDimIntVarArray(IloEnv &env, int dim4, int min, int max, const string &name, const string &index) {

    OneDimIntArray result = OneDimIntArray(env, dim4, min, max);
    string variableName = name
                          + "_" + index;
    result.setNames(variableName.c_str());

    return result;
}

OneDimNumArray initOneDimNumVarArray(IloEnv &env, int dim4, int min, int max, const string &name, const string &index) {


    OneDimNumArray result = OneDimNumArray(env, dim4, min, max);
    string variableName = name
                          + "_" + index;
    result.setNames(variableName.c_str());

    return result;
}

void IlpPatrolScheduler::run() {
    IloEnv env;
    IloModel model(env);

    // Asserted when car c visits location l at its vth visit
    ThreeDimIntArray x = initThreeDimIntVarArray(env, numberOfCars_, numberOfLocations_, maxCarVisits_, 0, 1, "x",
                                                 {"c", "l", "v"});

    // Assereted when car c serves location l at its vth visits at the location's vth visit.
    FourDimIntArray y = initFourDimIntVarArray(env, numberOfCars_, numberOfLocations_, maxCarVisits_, maxLocSessions_,
                                               0,
                                               1, "y", {"c", "l", "v", "s"});

    // the time car c will arrive to its vth location it will visit
    TwoDimNumArray tauCA = initTwoDimNumVarArray(env, numberOfCars_, maxCarVisits_, 0, Tmax_ - 120, "tauCA",
                                                 {"c", "v"});

    // The time car c will patrol it vth visit
    TwoDimNumArray tauCP = initTwoDimNumVarArray(env, numberOfCars_, maxCarVisits_, 0, 120, "tauCP", {"c", "v"});

    // The time a car will arrive the location vth visit
    TwoDimNumArray tauLA = initTwoDimNumVarArray(env, numberOfLocations_, maxLocSessions_, 0, Tmax_ - 120, "tauLA",
                                                 {"l", "s"});

    // The number of locations (non-distinct) car c will visit.
    OneDimIntArray Nc = initOneDimIntVarArray(env, numberOfCars_, 0, maxCarVisits_, "Nc", "c");

    // The number of time locatioin l will be served.
    OneDimIntArray Nl = initOneDimIntVarArray(env, numberOfLocations_, 0, maxLocSessions_, "Nl", "l");



    // C1: The first visit of a car is its initial location.
    for (int c = 0; c < numberOfCars_; ++c) {
        IloConstraint c1 = x[c][carsInitialLocations_[c]][0] == 1;
        string name = "c1_" + to_string(c);
        c1.setName(name.c_str());
        model.add(c1);
    }

    // C2: A car can not patrol a location unless it visits it.
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int l = 0; l < numberOfLocations_; ++l) {
            for (int v = 0; v < maxCarVisits_; ++v) {
                for (int s = 0; s < maxLocSessions_; ++s) {
                    IloConstraint c2 = y[c][l][v][s] <= x[c][l][v];
                    string name = "c2_c" + to_string(c)
                                  + "_l" + to_string(l)
                                  + "_v" + to_string(v)
                                  + "_s" + to_string(s);
                    c2.setName(name.c_str());
                    model.add(c2);
                }
            }
        }
    }

    // C3: A car can be only in one location at a time.
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int v = 0; v < maxCarVisits_; ++v) {
            IloExpr sum(env);
            for (int l = 0; l < numberOfLocations_; ++l) {
                sum += x[c][l][v];
            }
            IloConstraint c3 = sum == 1;
            string name = "c3_c" + to_string(c)
                          + "_v" + to_string(v);
            c3.setName(name.c_str());
            model.add(c3);
        }
    }

    // C4: A car can not move from location to another unless there is a direct path between the two locations
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int v = 1; v < maxCarVisits_; ++v) {
            for (int l1 = 0; l1 < numberOfLocations_; ++l1) {
                IloExpr sum(env);
                for (int l2 = 0; l2 < numberOfLocations_; ++l2) {
                    sum += x[c][l2][v - 1] * adjMatrix_[l2][l1];
                }
                IloConstraint c4 = x[c][l1][v] <= sum;
                string name = "c4_c" + to_string(c)
                              + "_v" + to_string(v)
                              + "_l" + to_string(l1);
                c4.setName(name.c_str());
                model.add(c4);
            }
        }
    }


    // C5: Only one car can serve one location at a time
    for (int l = 0; l < numberOfLocations_; ++l) {
        for (int s = 0; s < maxLocSessions_; ++s) {
            IloExpr sum(env);
            for (int c = 0; c < numberOfCars_; ++c) {
                for (int v = 0; v < maxCarVisits_; ++v) {
                    sum += y[c][l][v][s];
                }
            }
            IloConstraint c5 = sum <= 1;
            string name = "c5_l" + to_string(l)
                          + "_s" + to_string(s);

            c5.setName(name.c_str());
            model.add(c5);

        }
    }

    // C6: The time arriving to the location visited in the vth visit is equal
    // to the traverse time plus, the patrolling time plus the arrival
    // time to the previous location
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int v = 1; v < maxCarVisits_; ++v) {
            IloExpr sum(env);
            for (int l1 = 0; l1 < numberOfLocations_; ++l1) {
                for (int l2 = 0; l2 < numberOfLocations_; ++l2) {
                    if (l1 != l2) {
                        auto a = x[c][l1][v - 1] == 1;
                        a.setName(x[c][l1][v - 1].getName());
                        auto b = x[c][l2][v] == 1;
                        b.setName(x[c][l2][v].getName());
                        auto aAndB = a && b;
                        aAndB.setName((string(a.getName()) + "_AND_" + string(b.getName())).c_str());
                        sum += travelTime_[l1][l2] * aAndB;
                    }
                }
            }
            IloConstraint c6 = tauCA[c][v - 1] + tauCP[c][v - 1] + sum == tauCA[c][v];
            string name = "c7_c" + to_string(c)
                          + "_v" + to_string(v);
            c6.setName(name.c_str());
            model.add(c6);
        }
    }


    // C7: The time that a car c arrives to patrol a location l should be
    // before the time of the patrolling session and after the session before
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int l = 0; l < numberOfLocations_; ++l) {
            for (int v = 0; v < maxCarVisits_; ++v) {
                for (int s = 0; s < maxLocSessions_; ++s) {
                    IloNumVar L(env);
                    IloConstraint L1 = L <= 1000 * y[c][l][v][s];
                    string name = "c7aL1_c" + to_string(c)
                                  + "_l" + to_string(l)
                                  + "_v" + to_string(v)
                                  + "_s" + to_string(s);
                    L1.setName(name.c_str());
                    IloConstraint L2 = L <= tauCA[c][v];
                    name = "c7aL2_c" + to_string(c)
                           + "_l" + to_string(l)
                           + "_v" + to_string(v)
                           + "_s" + to_string(s);
                    L2.setName(name.c_str());
                    IloConstraint L3 = L >= 1000 * (y[c][l][v][s] - 1) + tauCA[c][v];
                    name = "c7aL3_c" + to_string(c)
                           + "_l" + to_string(l)
                           + "_v" + to_string(v)
                           + "_s" + to_string(s);
                    L3.setName(name.c_str());
                    IloConstraint c7a = L <= tauLA[l][s];
                    name = "c7a_c" + to_string(c)
                           + "_l" + to_string(l)
                           + "_v" + to_string(v)
                           + "_s" + to_string(s);
                    c7a.setName(name.c_str());
                    model.add(L1);
                    model.add(L2);
                    model.add(L3);
                    model.add(c7a);
                    if (s > 0) {
                        IloNumVar L(env);
                        IloConstraint L1 = L <= 1000 * y[c][l][v][s];
                        string name = "c7bL1_c" + to_string(c)
                                      + "_l" + to_string(l)
                                      + "_v" + to_string(v)
                                      + "_s" + to_string(s);
                        L1.setName(name.c_str());
                        IloConstraint L2 = L <= tauLA[l][s - 1];
                        name = "c7bL2_c" + to_string(c)
                               + "_l" + to_string(l)
                               + "_v" + to_string(v)
                               + "_s" + to_string(s);
                        L2.setName(name.c_str());
                        IloConstraint L3 = L >= 1000 * (y[c][l][v][s] - 1) + tauLA[l][s - 1];
                        name = "c7bL3_c" + to_string(c)
                               + "_l" + to_string(l)
                               + "_v" + to_string(v)
                               + "_s" + to_string(s);
                        L3.setName(name.c_str());
                        IloConstraint c7b = tauCA[c][v] >= L + y[c][l][v][s] * (taul_[l] + taulg_[l]);
                        name = "c7b_c" + to_string(c)
                               + "_l" + to_string(l)
                               + "_v" + to_string(v)
                               + "_s" + to_string(s);
                        c7b.setName(name.c_str());
                        model.add(L1);
                        model.add(L2);
                        model.add(L3);
                        model.add(c7b);
                    }
                }
            }
        }
    }

    // C8: The patrolling time of car c should exceed the minimum required patrolling time of the location
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int l = 0; l < numberOfLocations_; ++l) {
            for (int v = 0; v < maxCarVisits_; ++v) {
                for (int s = 0; s < maxLocSessions_; ++s) {
                    IloConstraint c8 = y[c][l][v][s] * taul_[l] <= tauCP[c][v];
                    string name = "c8_c" + to_string(c)
                                  + "_l" + to_string(l)
                                  + "_v" + to_string(v)
                                  + "_s" + to_string(s);
                    c8.setName(name.c_str());
                    model.add(c8);
                }
            }
        }
    }

    // C9: A location cannot be served more than the number of possible sessions
    for (int l = 0; l < numberOfLocations_; ++l) {
        for (int s = 0; s < maxLocSessions_; ++s) {
            IloExpr sum(env);
            for (int c = 0; c < numberOfCars_; ++c) {
                for (int v = 0; v < maxCarVisits_; ++v) {
                    sum += y[c][l][v][s];
                }
            }
            IloConstraint c9 = sum == (s < Nl[l]);

            string name = "c9_l" + to_string(l)
                          + "_s" + to_string(s);
            c9.setName(name.c_str());
            model.add(c9);
        }
    }



    // C10: The gap between two visits in one location should be greater than taulg_
    for (int l = 0; l < numberOfLocations_; ++l) {
        for (int s = 1; s < maxLocSessions_; ++s) {
            IloConstraint c10 = tauLA[l][s] >= (s < Nl[l]) * (taul_[l] + taulg_[l]) + tauLA[l][s - 1];
            string name = "c10_l" + to_string(l)
                          + "_s" + to_string(s);
            c10.setName(name.c_str());
            model.add(c10);
        }
    }

    // C11: The amount of time a car patrols a location should exceed the minimum requirement
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int l = 0; l < numberOfLocations_; ++l) {
            for (int v = 0; v < maxCarVisits_; ++v) {
                for (int s = 0; s < maxLocSessions_; ++s) {
                    IloNumVar L(env);
                    IloConstraint L1 = L <= 1000 * y[c][l][v][s];
                    string name = "c11bL1_c" + to_string(c)
                                  + "_l" + to_string(l)
                                  + "_v" + to_string(v)
                                  + "_s" + to_string(s);
                    L1.setName(name.c_str());
                    IloConstraint L2 = L <= tauLA[l][s];
                    name = "c11bL2_c" + to_string(c)
                           + "_l" + to_string(l)
                           + "_v" + to_string(v)
                           + "_s" + to_string(s);
                    L2.setName(name.c_str());
                    IloConstraint L3 = L >= 1000 * (y[c][l][v][s] - 1) + tauLA[l][s];
                    name = "c11bL3_c" + to_string(c)
                           + "_l" + to_string(l)
                           + "_v" + to_string(v)
                           + "_s" + to_string(s);
                    L3.setName(name.c_str());
                    auto c11 = tauCA[c][v] + tauCP[c][v] >= taul_[l] * y[c][l][v][s] + L;
                    name = "c11_c" + to_string(c)
                           + "_l" + to_string(l)
                           + "_v" + to_string(v)
                           + "_s" + to_string(s);
                    c11.setName(name.c_str());
                    model.add(L1);
                    model.add(L2);
                    model.add(L3);
                    model.add(c11);
                }
            }
        }
    }

    // C12: A car should visit the depot at least once.
    for (int c = 0; c < numberOfCars_; ++c) {
        IloExpr sum(env);
        for (int v = 0; v < maxCarVisits_; ++v) {
            for (int s = 0; s < numberOfCars_; ++s) {
                sum += y[c][depot_][v][s];
            }
        }
        IloConstraint c12 = sum == 1;
        auto name = "c12_c" + to_string(c);
        c12.setName(name.c_str());
        model.add(c12);
    }

    // C13: A car should stay in the depot for the required amount of time.
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int v = 0; v < maxCarVisits_; ++v) {
            IloExpr sum(env);
            for (int s = 0; s < numberOfCars_; ++s) {
                sum += y[c][depot_][v][s];
            }
            IloConstraint c13 = tauCP[c][v] >= restTime_[c] * sum;
            auto name = "c13_c" + to_string(c) + "_v" + to_string(v);
            c13.setName(name.c_str());
            model.add(c13);
        }


    }

    // C14: The car break time should end at time.
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int v = 0; v < maxCarVisits_; ++v) {
            IloExpr sum(env);
            for (int s = 0; s < maxLocSessions_; ++s) {
                IloNumVar La(env);
                IloConstraint L1a = La <= 1000 * y[c][depot_][v][s];
                string name = "c14aL1_c" + to_string(c)

                              + "_v" + to_string(v)
                              + "_s" + to_string(s);
                L1a.setName(name.c_str());
                IloConstraint L2a = La <= tauCA[c][v];
                name = "c14aL2_c" + to_string(c)

                       + "_v" + to_string(v)
                       + "_s" + to_string(s);
                L2a.setName(name.c_str());
                IloConstraint L3a = La >= 1000 * (y[c][depot_][v][s] - 1) + tauCA[c][v];
                name = "c14aL3_c" + to_string(c)

                       + "_v" + to_string(v)
                       + "_s" + to_string(s);
                L3a.setName(name.c_str());

                IloNumVar Lb(env);
                IloConstraint L1b = Lb <= 1000 * y[c][depot_][v][s];
                name = "c14bL1_c" + to_string(c)

                       + "_v" + to_string(v)
                       + "_s" + to_string(s);
                L1b.setName(name.c_str());
                IloConstraint L2b = Lb <= tauCP[c][v];
                name = "c14bL2_c" + to_string(c)

                       + "_v" + to_string(v)
                       + "_s" + to_string(s);
                L2b.setName(name.c_str());
                IloConstraint L3b = Lb >= 1000 * (y[c][depot_][v][s] - 1) + tauCP[c][v];
                name = "c14bL3_c" + to_string(c)

                       + "_v" + to_string(v)
                       + "_s" + to_string(s);
                L3b.setName(name.c_str());
                model.add(L1a);
                model.add(L2a);
                model.add(L3a);
                model.add(L1b);
                model.add(L2b);
                model.add(L3b);
                sum += La + Lb;
            }
            IloConstraint c14 = sum <= carsBreakEndTime_[c];
            auto name = "c14_c" + to_string(c) + "_v" + to_string(v);
            c14.setName(name.c_str());
            model.add(c14);
        }
    }

    // C15: A car should enter its break after the break start time.
    for (int c = 0; c < numberOfCars_; ++c) {
        for (int v = 0; v < maxCarVisits_; ++v) {
            IloExpr sum(env);
            for (int s = 0; s < numberOfCars_; ++s) {
                sum += y[c][depot_][v][s];
            }
            IloConstraint c15 = tauCA[c][v] >= carsBreakStartTime_[c] * sum;
            auto name = "c15_c" + to_string(c) + "_v" + to_string(v);
            c15.setName(name.c_str());
            model.add(c15);
        }
    }

    IloExpr obj(env);
    for (int l = 0; l < numberOfLocations_; ++l) {
        if (l != depot_) {
            obj = obj + Nl[l];
        }

    }


    model.add(IloMaximize(env, obj));


    IloCplex cplex(model);
    cplex.exportModel("model.lp");
    try {
        cplex.solve();
    } catch (IloCplex::Exception &e) {
        env.out() << e << endl;
    }

    if (cplex.getStatus() == IloAlgorithm::Infeasible) {
        env.out() << "No Solution" << endl;
    } else {
        env.out() << "Solution status: " << cplex.getStatus()
                  << endl;


        env.out() << "optimum = " << cplex.getObjValue() << endl;

        cout << endl;
        for (int c = 0; c < numberOfCars_; ++c) {
            cout << "Car 1 trip:" << endl;
            for (int v = 0; v < maxCarVisits_; ++v) {
                for (int l = 0; l < numberOfLocations_; ++l) {
                    auto xValue = cplex.getValue(x[c][l][v]);
                    if (xValue == 1) {
                        auto tauCAValue = cplex.getValue(tauCA[c][v]);
                        cout << "Location " << l << " was arrived at minute " << tauCAValue << " in visit #" << v << endl;

                        for (int s = 0; s < maxLocSessions_; ++s) {
                            auto yValue = cplex.getValue(y[c][l][v][s]);
                            if (yValue == 1) {
                                auto tauLAValue = cplex.getValue(tauLA[l][s]);
                                auto tauCPValue = cplex.getValue(tauCP[c][v]);
                                cout << "Location " << l << " was patrolled for " << tauCPValue << " minutes starting from minute "
                                     << tauLAValue << endl;
                            }
                        }


                    }
                }
                cout << endl;
            }
        }

        cout << endl;

    }

}

void IlpPatrolScheduler::setAdjMatrix(const vector<vector<int>> &adjMatrix) {
    IlpPatrolScheduler::adjMatrix_ = adjMatrix;
}

void IlpPatrolScheduler::setDopot(int dopot) {
    IlpPatrolScheduler::depot_ = dopot;
}

void IlpPatrolScheduler::setTMax(int tMax) {
    Tmax_ = tMax;
}

void IlpPatrolScheduler::setOMax(const vector<int> &oMax) {
    O_max_ = oMax;
}

void IlpPatrolScheduler::setSMax(const vector<int> &sMax) {
    S_max_ = sMax;
}

void IlpPatrolScheduler::setPatrolTime(const vector<int> &patrolTime) {
    IlpPatrolScheduler::patrolTime_ = patrolTime;
}

void IlpPatrolScheduler::setResTime(const vector<int> &resTime) {
    IlpPatrolScheduler::restTime_ = resTime;
}

void IlpPatrolScheduler::setNumberOfCars(int numberOfCars) {
    IlpPatrolScheduler::numberOfCars_ = numberOfCars;
}

void IlpPatrolScheduler::setCarAvailability(const vector<double> &carAvailability) {
    IlpPatrolScheduler::carAvailability_ = carAvailability;
}

void IlpPatrolScheduler::setTravelTime(const vector<vector<double>> &travelTime) {
    travelTime_ = travelTime;
}

void IlpPatrolScheduler::setDepot(int depot) {
    depot_ = depot;
}

void IlpPatrolScheduler::setRestTime(const vector<int> &restTime) {
    restTime_ = restTime;
}

void IlpPatrolScheduler::setMaxCarVisits(int maxCarVisits) {
    maxCarVisits_ = maxCarVisits;
}

void IlpPatrolScheduler::setMaxLocSessions(int maxLocSessions) {
    maxLocSessions_ = maxLocSessions;
}

void IlpPatrolScheduler::setNumberOfLocations(int numberOfLocations) {
    numberOfLocations_ = numberOfLocations;
}

void IlpPatrolScheduler::setTaul(const vector<double> &taul) {
    taul_ = taul;
}

void IlpPatrolScheduler::setTaulg(const vector<double> &taulg) {
    taulg_ = taulg;
}

void IlpPatrolScheduler::setCarsInitialLocations(const vector<int> &carsInitialLocations) {
    carsInitialLocations_ = carsInitialLocations;
}

void IlpPatrolScheduler::setCarsBreakStartTime(const vector<double> &carsBreakStartTime) {
    carsBreakStartTime_ = carsBreakStartTime;
}

void IlpPatrolScheduler::setCarsBreakEndTime(const vector<double> &carsBreakEndTime) {
    carsBreakEndTime_ = carsBreakEndTime;
}
