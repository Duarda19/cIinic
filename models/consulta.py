import json
import datetime

class Consulta:
  def __init__(self, id, data, confirmado, id_paciente, id_medico):
    self.__id = id
    self.__data = data
    self.__confirmado = confirmado
    self.__id_paciente = id_paciente
    self.__id_medico = id_medico

  def get_id(self): return self.__id
  def get_data(self): return self.__data
  def get_confirmado(self): return self.__confirmado
  def get_id_paciente(self): return self.__id_paciente
  def get_id_medico(self): return self.__id_medico

  def set_id(self, id): self.__id = id
  def set_data(self, data): self.__data = data
  def set_confirmado(self, confirmado): self.__confirmado = confirmado
  def set_id_paciente(self, id_paciente): self.__id_paciente = id_paciente
  def set_id_medico(self, id_medico): self.__id_medico = id_medico

  def __eq__(self, x):
    if self.__id == x.__id and self.__data == x.__data and self.__confirmado == x.__confirmado and self.__id_paciente == x.__id_paciente and self.__id_medico == x.__id_medico:
      return True
    return False

  def __str__(self):
    return f"{self.__id} - {self.__data.strftime('%d/%m/%Y %H:%M')} - {self.__confirmado} - {self.__id_paciente} - {self.__id_medico}"

  def to_json(self):
    return {
      'id': self.__id,
      'data': self.__data.strftime('%d/%m/%Y %H:%M'),
      'confirmado': self.__confirmado,
      'id_paciente': self.__id_paciente,
      'id_medico': self.__id_medico}


class NConsulta:
  __consultas = []

  @classmethod
  def inserir(cls, obj):
    cls.abrir()
    id = 0
    for aux in cls.__consultas:
      if aux.get_id() > id: id = aux.get_id()
    obj.set_id(id + 1)
    cls.__consultas.append(obj)
    cls.salvar()

  @classmethod
  def listar(cls):
    cls.abrir()
    return cls.__consultas

  @classmethod
  def listar_nao_confirmados(cls):
    cls.abrir()
    nao_confirmados = []
    aux = datetime.datetime.now()
    hoje = datetime.datetime(aux.year, aux.month, aux.day)
    for aux in cls.__consulta:
      if not aux.__confirmado and aux.__data > hoje:
        nao_confirmados.append(aux)
    return nao_confirmados

  @classmethod
  def listar_id(cls, id):
    cls.abrir()
    for obj in cls.__consultas:
      if obj.get_id() == id: return obj
    return None

  @classmethod
  def atualizar(cls, obj):
    cls.abrir()
    aux = cls.listar_id(obj.get_id())
    if aux is not None:
      aux.set_data(obj.get_data())
      aux.set_confirmado(obj.get_confirmado())
      aux.set_id_paciente(obj.get_id_paciente())
      aux.set_id_medico(obj.get_id_medico())
      cls.salvar()

  @classmethod
  def excluir(cls, obj):
    cls.abrir()
    aux = cls.listar_id(obj.get_id())
    if aux is not None:
      cls.__consultas.remove(aux)
      cls.salvar()

  @classmethod
  def abrir(cls):
    cls.__consultas = []
    try:
      with open("consultas.json", mode="r") as arquivo:
        consultas_json = json.load(arquivo)
        for obj in consultas_json:
          aux = Consulta(
            obj["id"],
            datetime.datetime.strptime(obj["data"], "%d/%m/%Y %H:%M"),
            obj["confirmado"], 
            obj["id_paciente"], 
            obj["id_medico"])
          cls.__consultas.append(aux)
    except FileNotFoundError:
      pass

  @classmethod
  def salvar(cls):
    with open("consultas.json", mode="w") as arquivo:
      json.dump(cls.__consultas, arquivo, default=Consulta.to_json)
