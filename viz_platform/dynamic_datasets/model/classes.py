import numpy as np
import scipy
import scipy.special
import scipy.interpolate
import pickle
import sklearn

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import MySQLdb
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.ext.mutable
from sqlalchemy import Table, Column, Integer, String, Binary, Float, Boolean, Enum, ForeignKey, PickleType, DateTime, LargeBinary
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy.types as types

Base = declarative_base()

scenario_x_ensemble = Table('scenario_x_ensemble', Base.metadata,
    Column('scenario_id', Integer, ForeignKey('scenario.id')),
    Column('ensemble_id', Integer, ForeignKey('ensemble.id')))

deployment_x_instrument = Table('deployment_x_instrument', Base.metadata,
    Column('deployment_id', Integer, ForeignKey('deployment.id')),
    Column('instrument_id', Integer, ForeignKey('instrument.id')))

deployment_x_platform = Table('deployment_x_platform', Base.metadata,
    Column('deployment_id', Integer, ForeignKey('deployment.id')),
    Column('platform_id', Integer, ForeignKey('platform.id')))

opt_x_optParamType = Table('opt_x_optParamType', Base.metadata,
    Column('optimization_id', Integer, ForeignKey('optimization.id')),
    Column('optParamType_id', Integer, ForeignKey('operationalParameterType.id')))

opt_x_decisionType = Table('opt_x_decisionType', Base.metadata,
    Column('optimization_id', Integer, ForeignKey('optimization.id')),
    Column('decisionType_id', Integer, ForeignKey('decisionType.id')))

opt_x_modelParamType = Table('opt_x_modelParamType', Base.metadata,
    Column('optimization_id', Integer, ForeignKey('optimization.id')),
    Column('modelParamType_id', Integer, ForeignKey('modelParameterType.id')))

opt_x_stateVarType = Table('opt_x_stateVarType', Base.metadata,
    Column('optimization_id', Integer, ForeignKey('optimization.id')),
    Column('stateVarType_id', Integer, ForeignKey('stateVarType.id')))

opt_x_instrumentType = Table('opt_x_instrumentType', Base.metadata,
    Column('optimization_id', Integer, ForeignKey('optimization.id')),
    Column('instrumentType_id', Integer, ForeignKey('instrumentType.id')))

class Decision(Base):
  __tablename__ = 'decision'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  id_type       = Column(Integer, ForeignKey('decisionType.id'), primary_key=True )
  id_schedule   = Column(Integer, ForeignKey('schedule.id') )
  time          = Column(Float)
  value         = Column(PickleType)
  decisionType  = relationship( 'DecisionType', back_populates='decisions' )

class DecisionType(Base):
  __tablename__ = 'decisionType'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  name          = Column(String(128))
  decisions     = relationship( 'Decision', back_populates='decisionType' )
  opts          = relationship( 'Optimization', back_populates='decisionTypes', secondary=opt_x_decisionType )

class DecisionDependency(Base):
  __tablename__ = 'decisionDependency'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  id_subject    = Column(Integer, ForeignKey('decisionType.id') )
  id_object     = Column(Integer, ForeignKey('decisionType.id') )
  dec_subject   = relationship( 'DecisionType', foreign_keys=[id_subject] )
  dec_object    = relationship( 'DecisionType', foreign_keys=[id_object]  )

class Deployment(Base):
  __tablename__ = 'deployment'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  instruments   = relationship( 'Instrument', back_populates='deployment', secondary=deployment_x_instrument )
  platforms     = relationship( 'Platform', back_populates='deployment', secondary=deployment_x_platform )
  predictions   = relationship( 'PredictedDataset', back_populates='deployment' )
  observations  = relationship( 'ObservedDataset', back_populates='deployment' )

class Ensemble(Base):
  __tablename__ = 'ensemble'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  scenarios     = relationship( 'Scenario', back_populates='ensembles', secondary=scenario_x_ensemble )

class Instrument(Base):
  __tablename__ = 'instrument'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  id_type       = Column(Integer, ForeignKey('instrumentType.id') )
  name          = Column(String(256))
  type          = relationship( 'InstrumentType' )
  deployment    = relationship( 'Deployment', back_populates='instruments', secondary=deployment_x_instrument )
  objFuncs      = relationship( 'ObjectiveFunction', back_populates='instrument' )

class InstrumentType(Base):
  __tablename__ = 'instrumentType'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  id_type       = Column(Integer, ForeignKey('stateVarType.id') )
  type          = relationship( 'StateVariableType' )
  opts          = relationship( 'Optimization', back_populates='instrumentTypes', secondary=opt_x_instrumentType )

class ModelParameter(Base):
  __tablename__  = 'modelParameter'
  id             = Column(Integer, primary_key=True, autoincrement=True)
  id_type        = Column(Integer, ForeignKey('modelParameterType.id'), primary_key=True )
  id_realization = Column(Integer, ForeignKey('realization.id') )
  value          = Column(Float)
  modelParamType = relationship( 'ModelParameterType', back_populates='modelParams' )
  realization    = relationship( 'Realization', back_populates='modelParams' )

class ModelParameterType(Base):
  __tablename__ = 'modelParameterType'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  name          = Column(String(64))	# pressure, aqueous CO2 content, total dissolved solids
  abvr          = Column(String(64))	# pf, co2, tds
  unit          = Column(String(64))	# kPa, %, kg/m3
  modelParams   = relationship( 'ModelParameter', back_populates='modelParamType' )
  opts          = relationship( 'Optimization', back_populates='modelParamTypes', secondary=opt_x_modelParamType )

class ObjectiveFunction(Base):
  __tablename__ = 'objFunction'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  id_instrument = Column(Integer, ForeignKey('instrument.id') )
  instrument    = relationship( 'Instrument', back_populates='objFuncs' )
  objVals       = relationship( 'ObjectiveValue', back_populates='objFunction' )

class ObjectiveValue(Base):
  __tablename__ = 'objValue'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  id_objectF    = Column(Integer, ForeignKey('objFunction.id') )
  id_simulation = Column(Integer, ForeignKey('simulation.id') )
  value         = Column(Float)
  objFunction   = relationship( 'ObjectiveFunction', back_populates='objVals' )
  simulation    = relationship( 'Simulation', back_populates='objVals' )

  def compute(self,time,end):
    observation = self.objFunction.instrument.deployment[0].observations[0]
    for prediction in self.objFunction.instrument.deployment[0].predictions:
      if prediction.simulation==self.simulation:
        f = scipy.interpolate.interp1d(time,prediction.data)
        err=0
        for i in range(observation.data.shape[0]):
          if time[i]<end:
            err += (f(observation.data[i,0])-observation.data[i,1])**2
        return err

class ObservedDataset(Base):
  __tablename__   = 'observedDataset'
  id              = Column(Integer, primary_key=True, autoincrement=True)
  id_deployment   = Column(Integer, ForeignKey('deployment.id') )
  id_stateVarType = Column(Integer, ForeignKey('stateVarType.id') )
  deployment      = relationship( 'Deployment', back_populates='observations' )
  stateVarType    = relationship( 'StateVariableType' )
  data            = Column(String(2**24))

class OperationalParameterType(Base):
  __tablename__ = 'operationalParameterType'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  name          = Column(String(64))
  abvr          = Column(String(64))
  unit          = Column(String(64))
  schedules     = relationship( 'Schedule', back_populates='optParamType' )
  opts          = relationship( 'Optimization', back_populates='optParamTypes', secondary=opt_x_optParamType )

class Optimization(Base):
  __tablename__   = 'optimization'
  id              = Column(Integer, primary_key=True, autoincrement=True)
  X               = Column(String(2**24))
  Y               = Column(String(2**24))
  Z               = Column(String(2**24))
  t               = Column(String(2**24))
  end             = Column(Float)
  optParamTypes   = relationship( 'OperationalParameterType', back_populates='opts', secondary=opt_x_optParamType )
  decisionTypes   = relationship( 'DecisionType', back_populates='opts', secondary=opt_x_decisionType )
  modelParamTypes = relationship( 'ModelParameterType', back_populates='opts', secondary=opt_x_modelParamType )
  stateVarTypes   = relationship( 'StateVariableType', back_populates='opts', secondary=opt_x_stateVarType )
  instrumentTypes = relationship( 'InstrumentType', back_populates='opts', secondary=opt_x_instrumentType )

  def generate_scenario(self,realization):
    scenario = Scenario(realization=realization)
    nInj = np.random.randint(1,3+1)
    nObs = np.random.randint(1,3+1)
    nInj = 2
    nObs = 2
    for iInj in range(nInj):
      pump_rates  = np.random.uniform(400,1000)
      start_time  = np.random.uniform(0.48*np.max(self.t),0.52*np.max(self.t))
      if iInj==0: start_time=0
      easting     = np.random.uniform(np.min(self.X),np.max(self.X))
      northing    = np.random.uniform(np.min(self.Y),np.max(self.Y))
      depth       = np.random.uniform(np.min(self.Z),np.max(self.Z))
      injWell     = Well(easting=easting,northing=northing,depth=depth,time=start_time)
      schedule    = Schedule(optParamType=self.optParamTypes[0],value=pump_rates,well=injWell)
      decisions   = [Decision(decisionType=self.decisionTypes[0])]
      scenario.schedules += [schedule]
    simulation  = Simulation(scenario=scenario)
    simulation.run(self.X,self.Y,self.Z,self.t,self.stateVarTypes[0])
    for iObs in range(nObs):
      if iObs==0:
        drill_time  = np.random.uniform(0.00*np.max(self.t),0.05*np.max(self.t))
      elif iObs==1:
        drill_time  = np.random.uniform(0.35*np.max(self.t),0.40*np.max(self.t))
      else:
        drill_time  = np.random.uniform(0.45*np.max(self.t),0.50*np.max(self.t))
      easting     = np.random.uniform(np.min(self.X),np.max(self.X))
      northing    = np.random.uniform(np.min(self.Y),np.max(self.Y))
      depth       = np.random.uniform(np.min(self.Z),np.max(self.Z))
      obsWell    = Well(easting=easting,northing=northing,depth=depth,time=drill_time)
      platform   = Platform(wells=[obsWell])
      sensor     = Instrument(type=self.instrumentTypes[0])
      deployment = Deployment(platforms=[platform],instruments=[sensor])
      prediction = PredictedDataset(deployment=deployment,stateVarType=self.stateVarTypes[0],simulation=simulation)
      prediction.compute(self.X,self.Y,self.Z,self.t)
      observed   = ObservedDataset(deployment=deployment,stateVarType=self.stateVarTypes[0],data=prediction.noisy_data(self.t,0.0005))
      objectiveFunction = ObjectiveFunction(instrument=sensor)
    return scenario

  def add_to_scenario(self,scenario,easting,northing,depth,drill_time):
    obsWell    = Well(easting=easting,northing=northing,depth=depth,time=drill_time)
    platform   = Platform(wells=[obsWell])
    sensor     = Instrument(type=self.instrumentTypes[0])
    deployment = Deployment(platforms=[platform],instruments=[sensor])
    prediction = PredictedDataset(deployment=deployment,stateVarType=self.stateVarTypes[0],simulation=scenario.simulations[0])
    prediction.compute(self.X,self.Y,self.Z,self.t)
    observed   = ObservedDataset(deployment=deployment,stateVarType=self.stateVarTypes[0],data=prediction.noisy_data(self.t,0.0005))
    objFunc    = ObjectiveFunction(instrument=sensor)
    return scenario

  def monte_carlo(self,schedules,deployments,full=False):
    T = np.random.uniform(0.2e+4,2.6e+4)
    S = np.random.uniform(0.5e-5,0.5e-2)
    #print T,S
    modelParams  = []
    modelParams += [ModelParameter(value=T,modelParamType=self.modelParamTypes[0])]
    modelParams += [ModelParameter(value=S,modelParamType=self.modelParamTypes[1])]
    realization  = Realization(modelParams=modelParams)
    scenario = Scenario(realization=realization)
    for true_schedule in schedules:
      pump_rates  = true_schedule.value
      start_time  = true_schedule.well.time
      easting     = true_schedule.well.easting
      northing    = true_schedule.well.northing
      depth       = true_schedule.well.depth
      injWell     = Well(easting=easting,northing=northing,depth=depth,time=start_time)
      schedule    = Schedule(optParamType=self.optParamTypes[0],value=pump_rates,well=injWell)
      decisions   = [Decision(decisionType=self.decisionTypes[0])]
      scenario.schedules += [schedule]
    simulation  = Simulation(scenario=scenario)
    if full: simulation.run(self.X,self.Y,self.Z,self.t,self.stateVarTypes[0])
    for true_deployment in deployments:
      obsWell    = true_deployment.platforms[0].wells[0]
      platform   = true_deployment.platforms[0]
      sensor     = true_deployment.instruments[0]
      deployment = true_deployment
      prediction = PredictedDataset(deployment=deployment,stateVarType=self.stateVarTypes[0],simulation=simulation)
      prediction.compute(self.X,self.Y,self.Z,self.t)
      objFunc = sensor.objFuncs[0]
      objVal  = ObjectiveValue(objFunction=objFunc,simulation=simulation)
    return scenario

  def mcmc(self,schedules,deployments,nn,full=False):
    scenarios = [self.monte_carlo(schedules,deployments)]
    nRej = 0
    while len(scenarios)<nn:
      print(len(scenarios))
      while True:
        step = 1-0.75/(1+np.exp(-2*(nRej-4)))
        T = scenarios[-1].realization.modelParams[0].value+np.random.normal(0,step*0.025e+4)
        S = scenarios[-1].realization.modelParams[1].value+np.random.normal(0,step*0.025e-3)
        if (0.2e+4<T<2.6e+4) and (0.5e-5<S<0.5e-2): break
      #print T,S
      modelParams  = []
      modelParams += [ModelParameter(value=T,modelParamType=self.modelParamTypes[0])]
      modelParams += [ModelParameter(value=S,modelParamType=self.modelParamTypes[1])]
      realization  = Realization(modelParams=modelParams)
      scenario = Scenario(realization=realization)
      for true_schedule in schedules:
        pump_rates  = true_schedule.value
        start_time  = true_schedule.well.time
        easting     = true_schedule.well.easting
        northing    = true_schedule.well.northing
        depth       = true_schedule.well.depth
        injWell     = Well(easting=easting,northing=northing,depth=depth,time=start_time)
        schedule    = Schedule(optParamType=self.optParamTypes[0],value=pump_rates,well=injWell)
        decisions   = [Decision(decisionType=self.decisionTypes[0])]
        scenario.schedules += [schedule]
      simulation  = Simulation(scenario=scenario)
      if full: simulation.run(self.X,self.Y,self.Z,self.t,self.stateVarTypes[0])
      for true_deployment in deployments:
        obsWell    = true_deployment.platforms[0].wells[0]
        platform   = true_deployment.platforms[0]
        sensor     = true_deployment.instruments[0]
        deployment = true_deployment
        prediction = PredictedDataset(deployment=deployment,stateVarType=self.stateVarTypes[0],simulation=simulation)
        prediction.compute(self.X,self.Y,self.Z,self.t)
        objFunc = sensor.objFuncs[0]
        objVal  = ObjectiveValue(objFunction=objFunc,simulation=simulation)

      # new
      e1new = scenario.simulations[0].objVals[0].compute(self.t,self.end)**0.5
      e2new = scenario.simulations[0].objVals[1].compute(self.t,self.end)**0.5
      # old
      e1old = scenarios[-1].simulations[0].objVals[0].compute(self.t,self.end)**0.5
      e2old = scenarios[-1].simulations[0].objVals[1].compute(self.t,self.end)**0.5

      #print e1,e3, e2,e4
      #print e1<=e3, e2<=e4
      acc1 = e1new<e1old and e2new<e2old
      acc2 = e1new<e1old and e2new>e2old and np.random.uniform(0,1)<(0.1+0.9*(e2new-e2old)/e2old)
      acc3 = e2new<e2old and e1new>e1old and np.random.uniform(0,1)<(0.1+0.9*(e1new-e1old)/e1old)
      acc4 = e1new>e1old and e2new>e2old and np.random.uniform(0,1)<(0.1+0.9*((e1new-e1old)/e1old+(e2new-e2old)/e2old))
      if acc1 or acc2 or acc3 or acc4:
        scenarios += [scenario]
        nRej = 0
      else:
        nRej+=1
    return scenarios

  def mcmc2(self,schedules,deployments,nn):
    scenarios = [self.monte_carlo(schedules,deployments)]
    nRej = 0
    while len(scenarios)<nn:
      print(len(scenarios))
      while True:
        step = 1-0.75/(1+np.exp(-2*(nRej-4)))
        T = scenarios[-1].realization.modelParams[0].value+np.random.normal(0,step*0.025e+4)
        S = scenarios[-1].realization.modelParams[1].value+np.random.normal(0,step*0.025e-3)
        if (0.2e+4<T<2.6e+4) and (0.5e-5<S<0.5e-2): break
      #print T,S
      modelParams  = []
      modelParams += [ModelParameter(value=T,modelParamType=self.modelParamTypes[0])]
      modelParams += [ModelParameter(value=S,modelParamType=self.modelParamTypes[1])]
      realization  = Realization(modelParams=modelParams)
      scenario = Scenario(realization=realization)
      for true_schedule in schedules:
        pump_rates  = true_schedule.value
        start_time  = true_schedule.well.time
        easting     = true_schedule.well.easting
        northing    = true_schedule.well.northing
        depth       = true_schedule.well.depth
        injWell     = Well(easting=easting,northing=northing,depth=depth,time=start_time)
        schedule    = Schedule(optParamType=self.optParamTypes[0],value=pump_rates,well=injWell)
        decisions   = [Decision(decisionType=self.decisionTypes[0])]
        scenario.schedules += [schedule]
      simulation  = Simulation(scenario=scenario)
      simulation.run(self.X,self.Y,self.Z,self.t,self.stateVarTypes[0])
      for true_deployment in deployments:
        obsWell    = true_deployment.platforms[0].wells[0]
        platform   = true_deployment.platforms[0]
        sensor     = true_deployment.instruments[0]
        deployment = true_deployment
        prediction = PredictedDataset(deployment=deployment,stateVarType=self.stateVarTypes[0],simulation=simulation)
        prediction.compute(self.X,self.Y,self.Z,self.t)
        objFunc = sensor.objFuncs[0]
        objVal  = ObjectiveValue(objFunction=objFunc,simulation=simulation)
      e1 = scenario.simulations[0].objVals[0].compute(self.t,self.end)**0.5
      e2 = scenario.simulations[0].objVals[1].compute(self.t,self.end)**0.5
      e3 = scenario.simulations[0].objVals[2].compute(self.t,self.end)**0.5
      e4 = scenarios[-1].simulations[0].objVals[0].compute(self.t,self.end)**0.5
      e5 = scenarios[-1].simulations[0].objVals[1].compute(self.t,self.end)**0.5
      e6 = scenarios[-1].simulations[0].objVals[2].compute(self.t,self.end)**0.5

      #print e1<=e3, e2<=e4
      if (e1<=e4 or e2<=e5 or e3<=e6):
        scenarios += [scenario]
        nRej = 0
      else:
        nRej+=1
    return scenarios

class Platform(Base):
  __tablename__ = 'platform'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  deployment    = relationship( 'Deployment', back_populates='platforms', secondary=deployment_x_platform )
  wells         = relationship( 'Well', back_populates='platform' )

class PredictedDataset(Base):
  __tablename__   = 'predictedDataset'
  id              = Column(Integer, primary_key=True, autoincrement=True)
  id_deployment   = Column(Integer, ForeignKey('deployment.id') )
  id_stateVarType = Column(Integer, ForeignKey('stateVarType.id') )
  id_simulation   = Column(Integer, ForeignKey('simulation.id') )
  deployment      = relationship( 'Deployment', back_populates='predictions' )
  stateVarType    = relationship( 'StateVariableType' )
  simulation      = relationship( 'Simulation', back_populates='predictions' )
  data            = Column(String(2**24))

  def stateVarField(self):
    for field in self.simulation.fields:
      if field.type==self.stateVarType: return field

  def compute(self,X,Y,Z,ts):
    #print type(self.stateVarField())
    self.data = np.zeros(ts.shape,dtype='float')
    if type(self.stateVarField())==type(None):
      #print 'compute just the sensor response'
      for schedule in self.simulation.scenario.schedules:
        Q = schedule.value
        T = self.simulation.scenario.realization.modelParams[0].value
        S = self.simulation.scenario.realization.modelParams[1].value
        xw = schedule.well.easting
        yw = schedule.well.northing
        zw = schedule.well.depth
        t0 = schedule.well.time
        xo = self.deployment.platforms[0].wells[0].easting
        yo = self.deployment.platforms[0].wells[0].northing
        zo = self.deployment.platforms[0].wells[0].depth
        r = ( (xw-xo)**2+(yw-yo)**2+(zw-zo)**2 )**0.5
        for it in range(len(ts)):
          self.data[it] += self.simulation.theis(Q,T,S,r,ts[it],t0)

    else:
      #print 'compute the full 4d response'
      data = pickle.loads(self.stateVarField().data)
      xw = self.deployment.platforms[0].wells[0].easting
      yw = self.deployment.platforms[0].wells[0].northing
      zw = self.deployment.platforms[0].wells[0].depth
      pts = np.array(list(zip(X.ravel(),Y.ravel(),Z.ravel())),dtype='float')
      for it in range(len(ts)):
        f = scipy.interpolate.LinearNDInterpolator(pts,data[:,:,:,it].ravel())
        self.data[it] = f(xw,yw,zw)

  def noisy_data(self,time,level):
    ii = np.where(time>self.deployment.platforms[0].wells[0].time)[0]
    return np.concatenate([ time[ii].reshape([len(ii),1]), (self.data[ii]+np.cumsum(np.random.normal(0,level,self.data[ii].shape))).reshape([len(ii),1]) ], axis=1)

class Realization(Base):
  __tablename__ = 'realization'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  modelParams   = relationship( 'ModelParameter', back_populates='realization' )
  scenarios     = relationship( 'Scenario', back_populates='realization' )

class Scenario(Base):
  __tablename__  = 'scenario'
  id             = Column(Integer, primary_key=True, autoincrement=True)
  id_realization = Column(Integer, ForeignKey('realization.id') )
  realization    = relationship( 'Realization', back_populates='scenarios' )
  schedules      = relationship( 'Schedule', back_populates='scenario' )
  ensembles      = relationship( 'Ensemble', back_populates='scenarios', secondary=scenario_x_ensemble )
  simulations    = relationship( 'Simulation', back_populates='scenario' )

class Schedule(Base):
  __tablename__   = 'schedule'
  id              = Column(Integer, primary_key=True, autoincrement=True)
  id_optParamType = Column(Integer, ForeignKey('operationalParameterType.id') )
  id_scenario     = Column(Integer, ForeignKey('scenario.id') )
  id_well         = Column(Integer, ForeignKey('well.id') )
  value           = Column(PickleType)
  optParamType    = relationship( 'OperationalParameterType', back_populates='schedules' )
  scenario        = relationship( 'Scenario', back_populates='schedules' )
  well            = relationship( 'Well', back_populates='schedules' )

class Simulation(Base):
  __tablename__  = 'simulation'
  id             = Column(Integer, primary_key=True, autoincrement=True)
  id_scenario    = Column(Integer, ForeignKey('scenario.id') )
  scenario       = relationship( 'Scenario', back_populates='simulations' )
  fields         = relationship( 'StateVariableField', back_populates='simulation' )
  predictions    = relationship( 'PredictedDataset', back_populates='simulation' )
  objVals        = relationship( 'ObjectiveValue', back_populates='simulation' )

  def theis(self,Q,T,S,r,t,t0):
    if t>t0:
      u = (r**2*S)/(4*T*(t-t0))
      W = -scipy.special.expi(-u)
      return Q / (4*np.pi*T) * W
    else: return 0.0

  def run(self,X,Y,Z,time,stateVarType):
    T = self.scenario.realization.modelParams[0].value
    S = self.scenario.realization.modelParams[1].value
    s = np.zeros([X.shape[0],Y.shape[1],Z.shape[2],time.shape[0]],dtype='float')
    for schedule in self.scenario.schedules:
      Q = schedule.value
      x = schedule.well.easting
      y = schedule.well.northing
      z = schedule.well.depth
      t0 = schedule.well.time
      for i in range(X.shape[0]):
        for j in range(Y.shape[1]):
          for k in range(X.shape[2]):
            r = ((X[i,j,k]-x)**2+(Y[i,j,k]-y)**2+(Z[i,j,k]-z)**2)**0.5
            for l in range(time.shape[0]):
              s[i,j,k,l] += self.theis(Q,T,S,r,time[l],t0)
    StateVariableField(type=stateVarType,simulation=self,data=pickle.dumps(s))

class StateVariableField(Base):
  __tablename__ = 'stateVarField'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  id_type       = Column(Integer, ForeignKey('stateVarType.id') )
  id_simulation = Column(Integer, ForeignKey('simulation.id') )
  data          = Column(String(2**26))
  type          = relationship( 'StateVariableType' )
  simulation    = relationship( 'Simulation', back_populates='fields' )

class StateVariableType(Base):
  __tablename__ = 'stateVarType'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  name          = Column(String(64))
  abvr          = Column(String(64))
  unit          = Column(String(64))
  opts          = relationship( 'Optimization', back_populates='stateVarTypes', secondary=opt_x_stateVarType )

class Well(Base):
  __tablename__   = 'well'
  id              = Column(Integer, primary_key=True, autoincrement=True)
  id_platform     = Column(Integer, ForeignKey('platform.id') )
  easting         = Column(Float)
  northing        = Column(Float)
  depth           = Column(Float)
  time            = Column(Float)
  platform        = relationship( 'Platform', back_populates='wells' )
  schedules       = relationship( 'Schedule', back_populates='well' )


class Forecast(Base):
  __tablename__ = 'forecast'
  id            = Column(Integer, primary_key=True, autoincrement=True)
  name          = Column(String(64))
  abvr          = Column(String(64))
  unit          = Column(String(64))


# %%
f = Forecast()
print(f)