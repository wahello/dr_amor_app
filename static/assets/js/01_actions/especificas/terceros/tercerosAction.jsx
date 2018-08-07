import {TERCERO_TYPES as TYPES} from '../../00_types';
import {
    fetchListGet,
    updateObject,
    fetchObject,
    callApiMethodPostParameters
} from '../../00_general_fuctions'

const current_url_api = 'terceros';

export const registrarIngresoTercero = (id, pin, options_action = {}) => {
    return (dispatch) => {
        let params = new URLSearchParams();
        params.append('pin', pin);
        const options = {...options_action, dispatch_method: dispatch};
        callApiMethodPostParameters(current_url_api, id, 'registrar_ingreso', params, options)
    }
};

export const registrarSalidaTercero = (id, pin, options_action = {}) => {
    return (dispatch) => {
        let params = new URLSearchParams();
        params.append('pin', pin);
        const options = {...options_action, dispatch_method: dispatch};
        callApiMethodPostParameters(current_url_api, id, 'registrar_salida', params, options)
    }
};

export const liquidarCuentaTercero = (id, pago, options_action = {}) => {
    return (dispatch) => {
        let params = new URLSearchParams();
        params.append('pago', JSON.stringify(pago));
        const options = {...options_action, dispatch_method: dispatch};
        callApiMethodPostParameters(current_url_api, id, 'liquidar_cuenta', params, options)
    }
};

export const fetchTercerosAusentes = (options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.fetch_all, payload: response})
        };
        const {limpiar_coleccion = true} = options_action;
        const options = {
            dispatches,
            ...options_action,
            dispatch_method: dispatch,
            clear_action_type: limpiar_coleccion ? TYPES.clear : null
        };
        fetchListGet(`${current_url_api}/listar_ausentes`, options);
    }
};

export const fetchTercerosPresentes = (options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.fetch_all, payload: response})
        };
        const {limpiar_coleccion = true} = options_action;
        const options = {
            dispatches,
            ...options_action,
            dispatch_method: dispatch,
            clear_action_type: limpiar_coleccion ? TYPES.clear : null
        };
        fetchListGet(`${current_url_api}/listar_presentes`, options);
    }
};

export const fetchTerceros = (options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.fetch_all, payload: response})
        };
        const {limpiar_coleccion = true} = options_action;
        const options = {
            dispatches,
            ...options_action,
            dispatch_method: dispatch,
            clear_action_type: limpiar_coleccion ? TYPES.clear : null
        };
        fetchListGet(current_url_api, options);
    }
};

export const fetchTercero = (id, options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.fetch, payload: response})
        };
        const options = {dispatches, ...options_action, dispatch_method: dispatch};
        fetchObject(current_url_api, id, options);
    }
};
export const clearTerceros = () => {
    return (dispatch) => {
        dispatch({type: TYPES.clear});

    }
};
export const updateTercero = (id, values, options_action = {}) => {
    return (dispatch) => {
        const dispatches = (response) => {
            dispatch({type: TYPES.update, payload: response})
        };
        const options = {dispatches, ...options_action, dispatch_method: dispatch};
        updateObject(current_url_api, id, values, options);
    }
};