import { WEBUI_BASE_URL } from '$lib/constants';

export type PaymentCreateRequest = {
	user_id: string;
	provider: string;
	amount: number;
	currency: string;
	description: string;
	return_url: string;
	method: string;
};

export type PaymentCreateResponse = {
	trx_id: string;
	order_id: string;
	user_id: string;
	provider: string;
	provider_reference_id: string;
	amount: number;
	currency: string;
	status: string;
	method: string;
	payment_url: string;
};

export type PaymentStatusResponse = {
	id: number;
	trx_id: string;
	order_id: string;
	user_id: string;
	provider: string;
	provider_reference_id: { String: string; Valid: boolean };
	amount: number;
	currency: string;
	status: string;
	payment_url: { String: string; Valid: boolean };
	expires_at: { Time: string; Valid: boolean };
	paid_at: { Time: string; Valid: boolean };
	failed_at: { Time: string; Valid: boolean };
	created_at: string;
	method: string;
	updated_at: string;
};

export const createPayment = async (
	token: string,
	body: PaymentCreateRequest
): Promise<PaymentCreateResponse> => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/v1/payments`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify(body)
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.error(err);
			error = err.detail ?? err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getPaymentStatus = async (
	token: string,
	trxId: string
): Promise<PaymentStatusResponse> => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/v1/payments/${trxId}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.error(err);
			error = err.detail ?? err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export type UserBalanceResponse = {
	id: string;
	balance: string;
	name: string;
	email: string;
};

export const getUserBalance = async (token: string): Promise<UserBalanceResponse> => {
	let error = null;

	const res = await fetch(`${WEBUI_BASE_URL}/api/v1/payments/balance`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.error(err);
			error = err.detail ?? err;
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};
