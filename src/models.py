from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)  # Considera usar hashing para contraseñas
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    fecha_de_subscripcion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    nombre: Mapped[str] = mapped_column(String(120))
    apellido: Mapped[str] = mapped_column(String(120))
    favoritos_planetas: Mapped[list["FavoritoPlaneta"]] = relationship("FavoritoPlaneta", back_populates="usuario")
    favoritos_personajes: Mapped[list["FavoritoPersonaje"]] = relationship("FavoritoPersonaje", back_populates="usuario")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "fecha_de_subscripcion": self.fecha_de_subscripcion.isoformat(),
            "nombre": self.nombre,
            "apellido": self.apellido
            # do not serialize the password, its a security breach
        }

class Planeta(db.Model):
    __tablename__ = 'planeta'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    clima: Mapped[str] = mapped_column(String(250))
    terreno: Mapped[str] = mapped_column(String(250))
    poblacion: Mapped[BigInteger] = mapped_column(BigInteger)
    favoritos: Mapped[list["FavoritoPlaneta"]] = relationship("FavoritoPlaneta", back_populates="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion
        }

class Personaje(db.Model):
    __tablename__ = 'personaje'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    altura: Mapped[str] = mapped_column(String(250))
    peso: Mapped[str] = mapped_column(String(250))
    genero: Mapped[str] = mapped_column(String(250))
    favoritos: Mapped[list["FavoritoPersonaje"]] = relationship("FavoritoPersonaje", back_populates="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "peso": self.peso,
            "genero": self.genero
        }

class FavoritoPlaneta(db.Model):
    __tablename__ = 'favorito_planeta'
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=False)
    planeta_id: Mapped[int] = mapped_column(ForeignKey('planeta.id'), nullable=False)
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="favoritos_planetas")
    planeta: Mapped["Planeta"] = relationship("Planeta", back_populates="favoritos")

    __table_args__ = (UniqueConstraint('usuario_id', 'planeta_id', name='unique_usuario_planeta'),)

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planeta_id": self.planeta_id
        }

class FavoritoPersonaje(db.Model):
    __tablename__ = 'favorito_personaje'
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey('personaje.id'), nullable=False)
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="favoritos_personajes")
    personaje: Mapped["Personaje"] = relationship("Personaje", back_populates="favoritos")

    __table_args__ = (UniqueConstraint('usuario_id', 'personaje_id', name='unique_usuario_personaje'),)

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personaje_id": self.personaje_id
        }

