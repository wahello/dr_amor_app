import {formatMoney} from 'accounting';
import moment from 'moment-timezone';
import momentLocaliser from "react-widgets-moment";

moment.tz.setDefault("America/Bogota");
moment.locale('es');
momentLocaliser(moment);

export const REGEX_SOLO_NUMEROS_DINERO = /^-{0,1}\d*\.{0,1}\d+$/;
export const REGEX_SOLO_NUMEROS = /^-{0,1}\d+$/;
export const REGEX_CORREO_ELECTRONICO = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

export const pesosColombianos = (plata) => formatMoney(Number(plata), "$", 0, ".", ",");
export const numerosFormato = (numero) => formatMoney(Number(numero), "", 0, ".", ",");
export const fechaFormatoUno = (fecha) => moment.tz(fecha, "America/Bogota").format('MMMM D [de] YYYY');
export const horaFormatoUno = (date) => moment.tz(date, "America/Bogota").format('hh:mm a');

export const upper = value => value && value.toUpperCase();
export const lower = value => value && value.toLowerCase();

export const tengoPermiso = (permisos, tipo = 'and') => {
    const mis_permisos = _.map(JSON.parse(localStorage.getItem('mis_permisos')), e => e.codename);
    let permisos_a_validar_array = permisos;
    if (!Array.isArray(permisos)) {
        permisos_a_validar_array = [permisos]
    }
    if (!Array.isArray(mis_permisos)) {
        permisos_a_validar_array = [mis_permisos]
    }
    const mis_permisos_array = _.map(mis_permisos, permiso => {
        return permiso
    });
    const validaciones_array = permisos_a_validar_array.map(permiso => {
        return mis_permisos_array.includes(permiso)
    });
    if (tipo === "and") {
        return !validaciones_array.includes(false);
    } else if (tipo === "or") {
        return validaciones_array.includes(true);
    }
};


export const permisosAdapter = (permisos_view) => {
    return _.mapValues(permisos_view, p => tengoPermiso(p));
};