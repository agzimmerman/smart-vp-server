import sys
# sys.path.append('/original_data/dynamic_datasets/model')

from .model.classes import *


def read_from_mysql_database(
        db_addr='localhost',
        db_user='miguel',
        db_pswd='passpass2',
        db_title='smart_doeFE',
):
    """ Return data in the following structure:
      - scenario
        - simulations
            - fields
                - data: e.g. pressure x, y, ?, time
                - simulations
            - predictions: e.g. synthetic well
                - data: e.g. pressure in teh synthetic well
                - deployment
                    - platforms
                        - wells
                            - easting
                            - northing
                            - time
                    - instruments
                    - observations
        - schedules: For MCMC realizations

    Args:
        db_addr:
        db_user:
        db_pswd:
        db_title:

    Returns:
        viz_platform.dynamic_datasets.model.classes.Scenario:

    Notes:
        Before being able to use this function it is necessary to set the
        following global variable in mysql mysql> SET global sql_mode="";

    """
    engine = _connect_to_MySQLdb(db_addr, db_pswd, db_title, db_user)
    _set_mysql_session(engine)

    plot = False
    plot = True

    nMC = 150
    nMCMC1 = 250
    nMCMC2 = 250

    X, Y, Z, time = _define_default_coords()

    modelParamTypes = []
    modelParamTypes += [
        ModelParameterType(name='Transmissivity', abvr='T', unit='ft2/day')]
    modelParamTypes += [ModelParameterType(name='Storativity', abvr='S', unit='1')]

    optParamTypes = [
        OperationalParameterType(name='Pumping Rate', abvr='Q', unit='bbl/day')]

    decisionTypes = []
    decisionTypes += [DecisionType(name='Drill New Well')]
    decisionTypes += [DecisionType(name='Install New Sensor')]
    decisionTypes += [DecisionType(name='Change Pumping Rate')]

    decisionDependencies = []
    decisionDependencies += [
        DecisionDependency(dec_subject=decisionTypes[0],
                           dec_object=decisionTypes[1])]
    decisionDependencies += [
        DecisionDependency(dec_subject=decisionTypes[0],
                           dec_object=decisionTypes[2])]

    stateVarTypes = [StateVariableType(name='Drawdown', abvr='s', unit='ft')]
    instrumentTypes = [InstrumentType(type=stateVarTypes[0])]

    modelParams = []
    modelParams += [ModelParameter(value=1.4e+4, modelParamType=modelParamTypes[0])]
    modelParams += [ModelParameter(value=0.3e-3, modelParamType=modelParamTypes[1])]

    truth = Realization(modelParams=modelParams)

    opt = Optimization(optParamTypes=optParamTypes, decisionTypes=decisionTypes,
                       stateVarTypes=stateVarTypes, modelParamTypes=modelParamTypes,
                       instrumentTypes=instrumentTypes, X=X, Y=Y, Z=Z, t=time,
                       end=0.4 * np.max(time))

    true_scenario = opt.generate_scenario(truth)
    return true_scenario


def _define_default_coords():
    x = np.linspace(0, 52800, 25)
    y = np.linspace(0, 52800, 25)
    z = np.linspace(-5280, 0, 2)
    time = np.logspace(-1, np.log10(2500), 30)  # days
    time = np.linspace(10, 2500, 100)  # days
    X, Y, Z = np.meshgrid(x, y, z)
    return X, Y, Z, time


def _set_mysql_session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()


def _connect_to_MySQLdb(db_addr, db_pswd, db_title, db_user):
    con = MySQLdb.connect(db_addr, db_user, db_pswd)
    cur = con.cursor()
    cur.execute("DROP DATABASE IF EXISTS %s" % db_title)
    con.commit()
    cur.execute("CREATE DATABASE %s" % db_title)
    cur.execute("USE %s" % db_title)
    con.commit()
    con.close()
    engine = sqlalchemy.create_engine(
        'mysql+mysqldb://%s:%s@localhost/%s' % (db_user, db_pswd, db_title),
        echo=False)
    return engine
