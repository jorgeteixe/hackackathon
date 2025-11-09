# Copyright (C) 2025-now  p.fernandezf <p@fernandezf.es> & iago.rivas <delthia@delthia.com>

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea los grupos base para la gestión de usuarios y asigna permisos"

    def add_arguments(self, parser): ...

    def handle(self, *args, **options):

        # Permisos específicos
        p_aceptar_participante = Permission.objects.filter(
            codename="aceptar_participante"
        ).first()
        if p_aceptar_participante is None:
            raise CommandError("Permiso 'aceptar_participante' inexistente")

        p_ver_cv_participante = Permission.objects.filter(
            codename="ver_cv_participante"
        ).first()
        if p_ver_cv_participante is None:
            raise CommandError("Permiso 'ver_cv_participante' inexistente")

        p_ver_dni_telefono_participante = Permission.objects.filter(
            codename="ver_dni_telefono_participante"
        ).first()
        if p_ver_dni_telefono_participante is None:
            raise CommandError("Permiso 'ver_dni_telefono_participante' inexistente")

        # Permisos globales
        add_all, change_all, delete_all, view_all = self._get_permisos_modelos()

        # Grupos
        permisos = {
            "Administradores": view_all
            + change_all
            + [
                p_aceptar_participante,
                p_ver_cv_participante,
                p_ver_dni_telefono_participante,
            ],
            "Revisores": view_all
            + [
                p_aceptar_participante,
                p_ver_cv_participante,
                p_ver_dni_telefono_participante,
            ],
            "Ver modelos de gestión": view_all,
        }

        for nombre, permisos_grupo in permisos.items():
            grupo, _creado = Group.objects.get_or_create(name=nombre)
            grupo.permissions.set(permisos_grupo)

            if _creado:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{nombre}' creado"))
            self.stdout.write(self.style.SUCCESS(f"Permisos asignados a '{nombre}'"))

    # Permisos genéricos para los modelos relevantes
    def _get_permisos_modelos(self):
        modelos = [
            "mentor",
            "participante",
            "pase",
            "patrocinador",
            "persona",
            "presencia",
            "restriccionalimentaria",
            "tipopase",
            "token",
        ]
        add_all = [
            Permission.objects.filter(codename=f"add_{m}").first() for m in modelos
        ]
        change_all = [
            Permission.objects.filter(codename=f"change_{m}").first() for m in modelos
        ]
        delete_all = [
            Permission.objects.filter(codename=f"delete_{m}").first() for m in modelos
        ]
        view_all = [
            Permission.objects.filter(codename=f"view_{m}").first() for m in modelos
        ]

        return add_all, change_all, delete_all, view_all
