import pandas as pd
import datetime
import urllib
import urllib.request
import json
import requests


class Reportes:
    def __init__(self):
        self.__cargar()
        self.lista_emisoras = self.diccionario.keys()
        self.estado = 'Reportes trimestrales'

    def __cargar(self):
        url = 'https://github.com/dabu-io/reportes_trimestrales_json/raw/main/reportes_trimestrales.json'
        datos = requests.get(url)
        self.diccionario = json.loads(datos.content)
        # print(self.diccionario)

    def __cargar_datos(self):
        dicc_local = {}
        emisora = self.emisora.upper()

        if self.emisora.upper() not in self.diccionario:
            dicc_series = {'ALFAA': 'ALFA', 'ALPEKA': 'ALEPK', 'AMXL': 'AMX', 'ASURB': 'ASUR',
                           'AUTLANB': 'AUTLAN', 'AXTELCPO': 'AXTEL', 'AZTECACPO': 'AZTECA',
                           'BIMBOA': 'BIMBO', 'BOLSAA': 'BOLSA', 'CEMEXCPO': 'CEMEX',
                           'CHDRAUIB': 'CHDRAUI', 'FEMSAUBD': 'FEMSA', 'GAPB': 'GAP', 'GCARSOA1': 'GCARSO',
                           'GFAMSAA': 'GFAMSA', 'GMEXICOB': 'GMEXICO', 'GRUMAB': 'GRUMA', 'GSANBORB-1': 'GSANBOR',
                           'KIMBERA': 'KIMBER', 'KOFUBL': 'KOF', 'KUOB': 'KUO', 'LABB': 'LAB', 'LALAB': 'LALA',
                           'LIVEPOLC-1': 'LIVEPOL', 'MFRISCOA-1': 'MFRISCO', 'NEMAKA': 'NEMAK', 'OMAB': 'OMA',
                           'PASAB': 'PASA', 'POCHTECB': 'POCHTEC', 'POSADASA': 'POSADAS', 'SIMECB': 'SIMEC',
                           'SITESB-1': 'SITES', 'SORIANAB': 'SORIANA', 'TLEVISACPO': 'TLEVISA', 'VITROA': 'VITRO',
                           'VOLARA': 'VOLAR'}
            emisora = dicc_series[self.emisora.upper()]

        for fecha in self.fechas:
            for concepto, valor in self.diccionario[emisora][self.estado][fecha][self.reporte].items():
                if concepto not in dicc_local:
                    dicc_local[concepto] = {}
                dicc_local[concepto][fecha] = valor
        return pd.DataFrame.from_dict(dicc_local, orient='index')

    def __rango_fechas(self):
        return pd.date_range(self.fechas[0], self.fechas[1], freq='Q').format()

    def balance(self, emisora, fechas, rango=False):
        '''
        PARAMETROS:
        -----------
        emisora : str
            Clave de emisora
        fecha : lista
            Lista con fechas (formato AAAA-mm-dd).
            Debe de incluir por lo menos dos fechas diferentes.
            El resultado se regresa en el órden que se ingresaron las fechas.
            Puedes utilizar un rango de fechas (inicio, fin).  Cambiar el parámetro "range" = True.
        range : bool
            Default = False.  Cambiarlo a True si estás usando un rango de fechas.
        Ejemplo utilizando rango de fechas:
            balance_g('amx', ['2019-01-01', '2019-12-31'], rango = True)'''
        self.emisora = emisora
        self.fechas = fechas
        self.rango = rango
        self.reporte = 'Balance'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()

    def resultados(self, emisora, fechas, rango=False):
        '''
        PARAMETROS:
        -----------
        emisora : str
            Clave de emisora
        fecha : lista
            Lista con fechas (formato AAAA-mm-dd).
            Debe de incluir por lo menos dos fechas diferentes.
            El resultado se regresa en el órden que se ingresaron las fechas.
            Puedes utilizar un rango de fechas (inicio, fin).  Cambiar el parámetro "range" = True.
        range : bool
            Default = False.  Cambiarlo a True si estás usando un rango de fechas.
        Ejemplo utilizando rango de fechas:
            resultados('amx', ['2019-01-01', '2019-12-31'], rango = True)
        '''
        self.emisora = emisora
        self.fechas = fechas
        self.rango = rango
        self.reporte = 'Income'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()


    def flujos(self, emisora, fechas, rango=False):
        '''
        PARAMETROS:
        -----------
        emisora : str
            Clave de emisora
        fecha : lista
            Lista con fechas (formato AAAA-mm-dd).
            Debe de incluir por lo menos dos fechas diferentes.
            El resultado se regresa en el órden que se ingresaron las fechas.
            Puedes utilizar un rango de fechas (inicio, fin).  Cambiar el parámetro "range" = True.
        range : bool
            Default = False.  Cambiarlo a True si estás usando un rango de fechas.
        Ejemplo utilizando rango de fechas:
            flujos('amx', ['2019-01-01', '2019-12-31'], rango = True)
        '''
        self.emisora = emisora
        self.fechas = fechas
        self.rango = rango
        self.reporte = 'CashFlows'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()


    def comparar(self, estado, fecha, acciones=''):
        '''
        PARAMETEROS:
        -----------
            De una lista de emisoras se compara un estado financieroen de un trimestre específico.
        estado : str
            El estado financiero a seleccionar ('balance_g', 'ingresos', 'flujos').
        fecha : str
            Una fecha en formato 'AAAA-mm-dd'.
        acciones : list
            Una lista con las acciones a analizar
        Ejemplo:
            comparar(estado='income', '2020-03-31', ['amx', 'femsa', 'ac', 'kof'])
        '''
        if len(acciones) == 0:
            acciones = self.lista_emisoras
        df_resultados = pd.DataFrame()
        lista_errores = []
        for accion in acciones:
            try:
                # Aquí quiero llamar al métedo seleccionado como si fuera una varibale pero no se
                # como hacerlo:  la idea es algo así df = datos.x(accion, [fecha, '2017-06-30'])
                # donde x es el estado financiero.  Por lo tanto voy a hacer un chorizo de if's
                if estado == 'balance':
                    df = self.balance(accion, [fecha, '2017-03-31'])
                elif estado == 'resultados':
                    df = self.resultados(accion, [fecha, '2017-03-31'])
                elif estado == 'flujos':
                    df = self.balance_g(accion, [fecha, '2017-03-31'])
            except:
                lista_errores.append(accion)
                continue
            df_resultados[accion] = df[fecha]

        return df_resultados


class Precios:
    '''
        PARAMETROS
        ----------
            emisoras : str, o lista
                La lista puede contener una o más emisoras.  Si la emisora cotiza utilizando una serie, esta debe
                de agregarse al parámetro.  Por ejemplo “CEMEXCPO”.
            fecha_inicial : str
                La fecha debe de ingresarse bajo el formato “AAAA-MM-DD”.  Por ejemplo "2020-12-15"
            fecha_final : str
                La fecha debe de ingresarse bajo el formato “AAAA-MM-DD”.  Por ejemplo "2020-12-15
            frecuencia : str, default '1d'
                La frecuencia puede ser diaria ('1d'), semanal ('1wk'), o mensual ('1mo')
            tipo_precio : str, default ‘Cierre Ajustado’
                En cado de consultar precios de dos o más acciones, solo se entrega el DataFrame
                con un tipo de precio.  Se puede cambiar el precio por “apertura”, “max”, “min”,
                “cierre” y "cierre ajustado"

        ALGUNAS LISTA DE EMISORAS
        --------
        Estas son algunas de las emisoras de la BMV que se pueden consultar
        'AC', 'AEROMEX', 'ALEATIC', 'ALFAA', 'ALPEKA', 'ALSEA', 'AMXL', 'ARA',
        'ASURB', 'AUTLANB', 'AXTELCPO', 'AZTECACPO', 'BIMBOA', 'BOLSAA', 'CEMEXCPO',
        'CHDRAUIB', 'CUERVO', 'ELEKTRA', 'ELEMENT', 'FEMSAUBD', 'GAPB', 'GCARSOA1',
        'GENTERA', 'GFAMSAA', 'GMEXICOB', 'GRUMAB', 'GSANBORB-1', 'HCITY', 'HERDEZ',
        'HOMEX', 'IENOVA', 'KIMBERA', 'KOFUBL', 'KUOB', 'LABB', 'LALAB', 'LIVEPOLC-1',
        'MFRISCOA-1', 'NEMAKA', 'OMAB', 'ORBIA', 'PAPPEL', 'PASAB', 'PE&OLES', 'PINFRA',
        'POCHTECB', 'POSADASA', 'SIMECB', 'SITESB-1','SORIANAB', 'TLEVISACPO','VITROA',
        'VOLARA','WALMEX'
    '''

    def __init__(self, emisora, inicio, final, frecuencia='1d', tipo_precio='cierre ajustado'):
        self.emisora = emisora
        self.inicio = inicio
        self.final = final
        self.frecuencia = frecuencia
        self.tipo_precio = tipo_precio
        self.__cierre()

    def __cierre(self):
        self.__tiempo_epoch()
        self.__verificar_orden()
        self.__tipo_entrada()
        self.__ejecutar()

    def __ejecutar(self):
        if self.entrada == list:
            self.__cargar_multiples()
        else:
            self.__cargar_emisora()

    def __tipo_entrada(self):
        if type(self.emisora) == list and len(self.emisora) > 1:
            self.entrada = type(self.emisora)
        elif type(self.emisora) == list:
            self.emisora = self.emisora[0]
            self.entrada = type(self.emisora)
        else:
            self.entrada = type(self.emisora)

    def __construccion_url(self):
        if self.emisora.upper() == 'IPC':
            self.url = f'https://query1.finance.yahoo.com/v7/finance/download/^MXX?period1={self.epoch0}&period2={self.epoch1}&interval={self.frecuencia}&events=history&includeAdjustedClose=true'
        else:
            self.url = f'https://query1.finance.yahoo.com/v7/finance/download/{self.emisora.upper()}.mx?period1={self.epoch0}&period2={self.epoch1}&interval={self.frecuencia}&events=history&includeAdjustedClose=true'

    def __tiempo_epoch(self):
        self.epoch0 = datetime.datetime.strptime(self.inicio, "%Y-%m-%d").date().strftime('%s')
        self.epoch1 = datetime.datetime.strptime(self.final, "%Y-%m-%d").date().strftime('%s')

    def __verificar_orden(self):
        if self.epoch0 > self.epoch1:
            raise Exception(f'Fecha final es menor a la fecha inicial.')

    def __crear_dataframe(self):
        rango_fechas = pd.date_range(self.inicio, self.final)
        return pd.DataFrame(index=rango_fechas)

    def __cargar_emisora(self):
        self.__construccion_url()
        df = pd.read_csv(self.url, index_col=0, parse_dates=True)
        df.rename(
            {'Open': 'Apertura', 'High': 'Máximo', 'Low': 'Mínimo', 'Close': 'Cierre', 'Adj Close': 'Cierre Ajustado'},
            axis=1, inplace=True)
        orden_columnas = ['Apertura', 'Máximo', 'Mínimo', 'Cierre', 'Cierre Ajustado']
        df = df.reindex(columns=orden_columnas)
        df.index.names = ['Fecha']
        df.sort_index(inplace=True)
        df.dropna(inplace=True)
        self.resultado = df

    def __cargar_multiples(self):
        df_precios = self.__crear_dataframe()
        self.lista = self.emisora.copy()
        for accion in self.lista:
            self.emisora = accion
            df = self.__cargar_emisora()
            df_precios = df_precios.join(self.resultado[self.tipo_precio.title()])
            df_precios.rename({self.tipo_precio.title(): accion.upper()}, axis=1, inplace=True)

        df_precios.dropna(how='all', inplace=True)
        df_precios.index.names = ['Fecha']
        self.resultado = df_precios


class Intradia:
    '''
     Parámetros
    ----------
        emisoras : str, o lista
            Ticker de la emisora.  La lista puede contener una o más emisoras.  Si la emisora cotiza
            utilizando una serie, esta debe de agregarse al parámetro.  Ejemplo “CEMEXCPO”.
        inicio : str
            La fecha debe de ingresarse bajo el formato “AAAA-MM-DD”.  Ejemplo "2020-12-12"
        final : str
            La fecha debe de ingresarse bajo el formato “AAAA-MM-DD”.  Ejemplo "2020-12-15
        Intervalo : str, default '1m' (1minuto)
            Se puede cambiar el intervalo de tiempo a '2m', '5m', '15m', '30m', '60m', '90m'

    IMPORTANTE
    ----------
    YAHOO FINANCE guarda datos hasta de 29 días de la fecha actual en intervalos de 1m

    Emisoras
    --------
    lista_emisoras =['AC', 'AEROMEX', 'ALEATIC', 'ALFAA', 'ALPEKA', 'ALSEA', 'AMXL', 'ARA',
                  'ASURB', 'AUTLANB', 'AXTELCPO', 'AZTECACPO', 'BIMBOA', 'BOLSAA', 'CEMEXCPO',
                  'CHDRAUIB', 'CUERVO', 'ELEKTRA', 'ELEMENT', 'FEMSAUBD', 'GAPB', 'GCARSOA1',
                  'GENTERA', 'GFAMSAA', 'GMEXICOB', 'GRUMAB', 'GSANBORB-1', 'HCITY', 'HERDEZ',
                  'HOMEX', 'IENOVA', 'KIMBERA', 'KOFUBL', 'KUOB', 'LABB', 'LALAB', 'LIVEPOLC-1',
                  'MFRISCOA-1', 'NEMAKA', 'OMAB', 'ORBIA', 'PAPPEL', 'PASAB', 'PE&OLES', 'PINFRA',
                  'POCHTECB', 'POSADASA', 'SIMECB', 'SITESB-1','SORIANAB', 'TLEVISACPO','VITROA',
                  'VOLARA','WALMEX']
   '''

    def __init__(self, emisora, inicio, final, intervalo='1m'):
        self.emisora = emisora
        self.inicio = inicio
        self.final = final
        self.intervalo = intervalo
        self.__intradia()

    def __intradia(self):
        self.__tiempo_epoch()
        self.__verificar_argumentos()
        self.__construccion_url()
        self.__cargar_intradia()

    def __tiempo_epoch(self):
        self.epoch0 = datetime.datetime.strptime(self.inicio, "%Y-%m-%d").date().strftime('%s')
        self.epoch1 = datetime.datetime.strptime(self.final, "%Y-%m-%d").date().strftime('%s')
        self.rango_fechas = pd.to_datetime(self.final).date() - pd.to_datetime(self.inicio).date()

    def __verificar_argumentos(self):
        if self.epoch1 < self.epoch0:
            raise Exception('Fecha final es menor a la fecha inicial.')
        elif self.rango_fechas > pd.Timedelta(7, 'days') and self.intervalo == '1m':
            raise Exception('Rango de periodo no debe de ser mayor a 7 dias para intervalo de 1m.')
        elif self.rango_fechas > pd.Timedelta(60, 'days'):
            raise Exception('Rango de periodo no debe de ser mayor a 60 dias.')
        elif self.intervalo not in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo',
                                    '3mo']:
            raise Exception(f'Intervalo invalido.  Intervalo seleccionado {self.intervalo}')

    def __construccion_url(self):
        if self.emisora.upper() == 'IPC':
            self.url = f'https://query1.finance.yahoo.com/v8/finance/chart/^MXX?period1={self.epoch0}&period2={self.epoch1}&interval={self.intervalo}'
        else:
            self.url = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.emisora.upper()}.mx?period1={self.epoch0}&period2={self.epoch1}&interval={self.intervalo}'

    def __cargar_intradia(self):
        datos_crudos = urllib.request.urlopen(self.url).read()
        datos_json = json.loads(datos_crudos)
        datos = datos_json['chart']['result'][0]
        timestamp = datos['timestamp']
        apertura = datos['indicators']['quote'][0]['open']
        maximo = datos['indicators']['quote'][0]['high']
        minimo = datos['indicators']['quote'][0]['low']
        cierre = datos['indicators']['quote'][0]['close']

        precios = pd.DataFrame(
            {'Fecha/Hora': timestamp, 'Apertura': apertura, 'Máximo': maximo, 'Mínimo': minimo, 'Cierre': cierre})
        # la hora original es GMT, para cambiarla a MX le resto 6 horas
        precios['Fecha/Hora'] = pd.to_datetime(precios['Fecha/Hora'], unit='s') + pd.Timedelta(-6, 'hours')

        precios.set_index('Fecha/Hora', inplace=True)
        self.resultado = precios


class Financials:
    def __init__(self):
        self.__cargar()
        self.lista_emisoras = self.diccionario.keys()
        self.estado = 'Quarterly Reports'

    def __cargar(self):
        url = 'https://github.com/dabu-io/reportes_trimestrales_json/raw/main/reportes_trimestrales.json'
        datos = requests.get(url)
        self.diccionario = json.loads(datos.content)

    def __cargar_datos(self):
        dicc_local = {}
        emisora = self.emisora.upper()

        if emisora not in self.diccionario:
            dicc_series = {'ALFAA': 'ALFA', 'ALPEKA': 'ALEPK', 'AMXL': 'AMX', 'ASURB': 'ASUR',
                           'AUTLANB': 'AUTLAN', 'AXTELCPO': 'AXTEL', 'AZTECACPO': 'AZTECA',
                           'BIMBOA': 'BIMBO', 'BOLSAA': 'BOLSA', 'CEMEXCPO': 'CEMEX',
                           'CHDRAUIB': 'CHDRAUI', 'FEMSAUBD': 'FEMSA', 'GAPB': 'GAP', 'GCARSOA1': 'GCARSO',
                           'GFAMSAA': 'GFAMSA', 'GMEXICOB': 'GMEXICO', 'GRUMAB': 'GRUMA', 'GSANBORB-1': 'GSANBOR',
                           'KIMBERA': 'KIMBER', 'KOFUBL': 'KOF', 'KUOB': 'KUO', 'LABB': 'LAB', 'LALAB': 'LALA',
                           'LIVEPOLC-1': 'LIVEPOL', 'MFRISCOA-1': 'MFRISCO', 'NEMAKA': 'NEMAK', 'OMAB': 'OMA',
                           'PASAB': 'PASA', 'POCHTECB': 'POCHTEC', 'POSADASA': 'POSADAS', 'SIMECB': 'SIMEC',
                           'SITESB-1': 'SITES', 'SORIANAB': 'SORIANA', 'TLEVISACPO': 'TLEVISA', 'VITROA': 'VITRO',
                           'VOLARA': 'VOLAR'}
            emisora = dicc_series[emisora]

        for fecha in self.fechas:
            for concepto, valor in self.diccionario[emisora][self.estado][fecha][self.reporte].items():
                if concepto not in dicc_local:
                    dicc_local[concepto] = {}
                dicc_local[concepto][fecha] = valor
        df = pd.DataFrame.from_dict(dicc_local, orient='index')
        return pd.DataFrame.from_dict(dicc_local, orient='index')

    def __rango_fechas(self):
        return pd.date_range(self.fechas[0], self.fechas[1], freq='Q').format()

    def balance(self, ticker, dates, range=False):
        '''
        PARAMETERS:
        -----------
        ticker :  str
            Security Name.
        dates : list
            Date list (YYYY-mm-dd format).
            Include at least two different dates.
            Date info are returned as listed.
            In order to use a date range (start, end) turn parameter "range" = True.  The date range will calculate
            the end of the quarter date for the start and end dates.
        range : bool
            Default = False.  Change it to True if you are using a date range.
        Example:
            balance_s('amx',['2019-01-01', '2019-12-31'], rango = True)
        '''

        self.emisora = ticker
        self.fechas = dates
        self.rango = range
        self.reporte = 'Balance'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()


    def income(self, ticker, dates, range=False):
        '''
        PARAMETERS:
        -----------
        ticker :  str
            Security Name.
        dates : list
            Date list (YYYY-mm-dd format).
            Include at least two different dates.
            Date info are returned as listed.
            In order to use a date range (start, end) turn parameter "range" = True.  The date range will calculate
            the end of the quarter date for the start and end dates.
        range : bool
            Default = False.  Change it to True if you are using a date range.
        Example:
            income('amx',['2019-01-01', '2019-12-31'], rango = True)
        '''

        self.emisora = ticker
        self.fechas = dates
        self.rango = range
        self.reporte = 'Income'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()

    def flows(self, ticker, dates, range=False):
        '''
        PARAMETERS:
        -----------
        ticker :  str
            Security Name.
        dates : list
            Date list (YYYY-mm-dd format).
            Include at least two different dates.
            Date info are returned as listed.
            In order to use a date range (start, end) turn parameter "range" = True.  The date range will calculate
            the end of the quarter date for the start and end dates.
        range : bool
            Default = False.  Change it to True if you are using a date range.
        Example:
            flows('amx',['2019-01-01', '2019-12-31'], rango = True)
        '''

        self.emisora = ticker
        self.fechas = dates
        self.rango = range
        self.reporte = 'CashFlows'
        if self.rango is True:
            self.fechas = self.__rango_fechas()
        return self.__cargar_datos()

    def compare(self, financial_statement, date, tickers=''):
        '''
        "compare" funtion compares a financial statement of two or more securities in a given quarter.
        PARAMETERS
        ----------
        financial_statement : str
            Financial statement to select ('balance_s', 'income', 'flows')
        date : str
            A end of the quarter date (YYYY-mm-dd format).
        tickers :  list
            A list of tickers to compare
        Example:
            compare('income', '2020-03-31', ['amx', 'femsa', 'ac', 'kof'])
        '''
        if len(tickers) == 0:
            tickers = self.lista_emisoras
        df_resultados = pd.DataFrame()
        lista_errores = []
        for ticker in tickers:
            try:
                # Aquí quiero llamar al métedo seleccionado como si fuera una varibale pero no se
                # como hacerlo:  la idea es algo así df = datos.x(ticker, [fecha, '2017-06-30'])
                # donde x es el estado financiero.  Por lo tanto voy a hacer un chorizo de if's
                if financial_statement == 'balance':
                    df = self.balance(ticker, [date, '2017-03-31'])
                elif financial_statement == 'income':
                    df = self.income(ticker, [date, '2017-03-31'])
                elif financial_statement == 'flows':
                    df = self.flows(ticker, [date, '2017-03-31'])
            except:
                lista_errores.append(ticker)
                continue
            df_resultados[ticker] = df[date]

        return df_resultados


class Price:
    '''
        PARAMETERS
        ----------
            ticker : str, o list
                List can contain one or more tickers.  If the ticker use a serie, it must be include it.
                Example:  CEMEX has the CPO series --->  CEMEXCPO
            start_date : str
                Date format "AAAA-mm-dd".  "2020-12-15"
            end_date : str
                Date format "AAAA-mm-dd".  "2020-12-15"
            frecuency : str, default '1d'
                Can be daily ('1d'), weekly ('1wk') or monthly ('1mo')
            price_type : str, default ‘Adj Close’
                When two or more stocks are called, the DataFrame will contain just one price. Defalut is
                "Adj Close", but it can be changed to 'Open', 'High', 'Low' and 'Close'

        SOME TICKER NAMES:
        --------
        'AC', 'AEROMEX', 'ALEATIC', 'ALFAA', 'ALPEKA', 'ALSEA', 'AMXL', 'ARA',
        'ASURB', 'AUTLANB', 'AXTELCPO', 'AZTECACPO', 'BIMBOA', 'BOLSAA', 'CEMEXCPO',
        'CHDRAUIB', 'CUERVO', 'ELEKTRA', 'ELEMENT', 'FEMSAUBD', 'GAPB', 'GCARSOA1',
        'GENTERA', 'GFAMSAA', 'GMEXICOB', 'GRUMAB', 'GSANBORB-1', 'HCITY', 'HERDEZ',
        'HOMEX', 'IENOVA', 'KIMBERA', 'KOFUBL', 'KUOB', 'LABB', 'LALAB', 'LIVEPOLC-1',
        'MFRISCOA-1', 'NEMAKA', 'OMAB', 'ORBIA', 'PAPPEL', 'PASAB', 'PE&OLES', 'PINFRA',
        'POCHTECB', 'POSADASA', 'SIMECB', 'SITESB-1','SORIANAB', 'TLEVISACPO','VITROA',
        'VOLARA','WALMEX'
    '''

    def __init__(self, ticker, start, end, freq='1d', price_type='Adj Close'):
        self.emisora = ticker
        self.inicio = start
        self.final = end
        self.frecuencia = freq
        self.tipo_precio = price_type
        self.__cierre()

    def __cierre(self):
        self.__tiempo_epoch()
        self.__verificar_orden()
        self.__tipo_entrada()
        self.__ejecutar()

    def __ejecutar(self):
        if self.entrada == list:
            self.__cargar_multiples()
        else:
            self.__cargar_emisora()

    def __tipo_entrada(self):
        if type(self.emisora) == list and len(self.emisora) > 1:
            self.entrada = type(self.emisora)
        elif type(self.emisora) == list:
            self.emisora = self.emisora[0]
            self.entrada = type(self.emisora)
        else:
            self.entrada = type(self.emisora)

    def __construccion_url(self):
        if self.emisora.upper() == 'IPC':
            self.url = f'https://query1.finance.yahoo.com/v7/finance/download/^MXX?period1={self.epoch0}&period2={self.epoch1}&interval={self.frecuencia}&events=history&includeAdjustedClose=true'
        else:
            self.url = f'https://query1.finance.yahoo.com/v7/finance/download/{self.emisora.upper()}.mx?period1={self.epoch0}&period2={self.epoch1}&interval={self.frecuencia}&events=history&includeAdjustedClose=true'

    def __tiempo_epoch(self):
        self.epoch0 = datetime.datetime.strptime(self.inicio, "%Y-%m-%d").date().strftime('%s')
        self.epoch1 = datetime.datetime.strptime(self.final, "%Y-%m-%d").date().strftime('%s')

    def __verificar_orden(self):
        if self.epoch0 > self.epoch1:
            raise Exception(f'Fecha final es menor a la fecha inicial.')

    def __crear_dataframe(self):
        rango_fechas = pd.date_range(self.inicio, self.final)
        return pd.DataFrame(index=rango_fechas)

    def __cargar_emisora(self):
        self.__construccion_url()
        df = pd.read_csv(self.url, index_col=0, parse_dates=True)
        # df.rename(
        #     {'Open': 'Apertura', 'High': 'Máximo', 'Low': 'Mínimo', 'Close': 'Cierre', 'Adj Close': 'Cierre Ajustado'},
        #     axis=1, inplace=True)
        orden_columnas = ['Open', 'High', 'Low', 'Close', 'Adj Close']
        df = df.reindex(columns=orden_columnas)
        # df.index.names = ['Fecha']
        df.sort_index(inplace=True)
        df.dropna(inplace=True)
        self.show = df

    def __cargar_multiples(self):
        df_precios = self.__crear_dataframe()
        self.lista = self.emisora.copy()
        for accion in self.lista:
            self.emisora = accion
            df = self.__cargar_emisora()
            df_precios = df_precios.join(self.show[self.tipo_precio.title()])
            df_precios.rename({self.tipo_precio.title(): accion.upper()}, axis=1, inplace=True)

        df_precios.dropna(how='all', inplace=True)
        df_precios.index.names = ['Fecha']
        df_precios.sort_index(axis=1, inplace=True)
        self.show = df_precios


class Intraday:
    '''
     PARAMETERS
    ----------
        ticker : str, o list
            List can contain one or more tickers.  If the ticker use a serie, it must be include it.
            Example:  CEMEX has the CPO series --->  CEMEXCPO
        start_date : str
            Date format "AAAA-mm-dd".  "2020-12-15"
        end_date : str
            Date format "AAAA-mm-dd".  "2020-12-15"
        Interval : str, default '1m' (1minute)
            It can be changed to '2m', '5m', '15m', '30m', '60m', '90m'

    IMPORTANT
    ----------
    Yahoo Finance keeps the last 29 days of 1m intervals.

    TICKERS
    --------
    tickers_list =['AC', 'AEROMEX', 'ALEATIC', 'ALFAA', 'ALPEKA', 'ALSEA', 'AMXL', 'ARA',
                  'ASURB', 'AUTLANB', 'AXTELCPO', 'AZTECACPO', 'BIMBOA', 'BOLSAA', 'CEMEXCPO',
                  'CHDRAUIB', 'CUERVO', 'ELEKTRA', 'ELEMENT', 'FEMSAUBD', 'GAPB', 'GCARSOA1',
                  'GENTERA', 'GFAMSAA', 'GMEXICOB', 'GRUMAB', 'GSANBORB-1', 'HCITY', 'HERDEZ',
                  'HOMEX', 'IENOVA', 'KIMBERA', 'KOFUBL', 'KUOB', 'LABB', 'LALAB', 'LIVEPOLC-1',
                  'MFRISCOA-1', 'NEMAKA', 'OMAB', 'ORBIA', 'PAPPEL', 'PASAB', 'PE&OLES', 'PINFRA',
                  'POCHTECB', 'POSADASA', 'SIMECB', 'SITESB-1','SORIANAB', 'TLEVISACPO','VITROA',
                  'VOLARA','WALMEX']
   '''

    def __init__(self, ticker, start, end, interval='1m'):
        self.emisora = ticker
        self.inicio = start
        self.final = end
        self.intervalo = interval
        self.__intradia()

    def __intradia(self):
        self.__tiempo_epoch()
        self.__verificar_argumentos()
        self.__construccion_url()
        self.__cargar_intradia()

    def __tiempo_epoch(self):
        self.epoch0 = datetime.datetime.strptime(self.inicio, "%Y-%m-%d").date().strftime('%s')
        self.epoch1 = datetime.datetime.strptime(self.final, "%Y-%m-%d").date().strftime('%s')
        self.rango_fechas = pd.to_datetime(self.final).date() - pd.to_datetime(self.inicio).date()

    def __verificar_argumentos(self):
        if self.epoch1 < self.epoch0:
            raise Exception('Start date grater than final date.')
        elif self.rango_fechas > pd.Timedelta(7, 'days') and self.intervalo == '1m':
            raise Exception('With "1m" interval, period range must be less than 7 days.')
        elif self.rango_fechas > pd.Timedelta(60, 'days'):
            raise Exception('Period range must be less than 60 days.')
        elif self.intervalo not in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo',
                                    '3mo']:
            raise Exception(f'Invalid interval')

    def __construccion_url(self):
        if self.emisora.upper() == 'IPC':
            self.url = f'https://query1.finance.yahoo.com/v8/finance/chart/^MXX?period1={self.epoch0}&period2={self.epoch1}&interval={self.intervalo}'
        else:
            self.url = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.emisora.upper()}.mx?period1={self.epoch0}&period2={self.epoch1}&interval={self.intervalo}'

    def __cargar_intradia(self):
        datos_crudos = urllib.request.urlopen(self.url).read()
        datos_json = json.loads(datos_crudos)
        datos = datos_json['chart']['result'][0]
        timestamp = datos['timestamp']
        apertura = datos['indicators']['quote'][0]['open']
        maximo = datos['indicators']['quote'][0]['high']
        minimo = datos['indicators']['quote'][0]['low']
        cierre = datos['indicators']['quote'][0]['close']

        precios = pd.DataFrame(
            {'Timestamp': timestamp, 'Open': apertura, 'High': maximo, 'Low': minimo, 'Close': cierre})
        # la hora original es GMT, para cambiarla a MX le resto 6 horas
        precios['Timestamp'] = pd.to_datetime(precios['Timestamp'], unit='s') + pd.Timedelta(-6, 'hours')

        precios.set_index('Timestamp', inplace=True)
        self.show = precios
