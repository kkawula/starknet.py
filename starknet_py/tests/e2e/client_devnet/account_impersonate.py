import pytest

from starknet_py.contract import Contract
from starknet_py.net.client_errors import ClientError


@pytest.mark.asyncio
async def test_impersonate_account(
    devnet_forking_mode_client, impersonated_account, f_string_contract
):
    await devnet_forking_mode_client.impersonate_account(
        address=impersonated_account.address
    )

    contract = await Contract.from_address(
        provider=impersonated_account, address=f_string_contract.address
    )

    invocation = await contract.functions["set_string"].invoke_v1(
        "test", auto_estimate=True
    )

    await devnet_forking_mode_client.stop_impersonate_account(
        address=impersonated_account.address
    )

    assert invocation.invoke_transaction.sender_address == impersonated_account.address


@pytest.mark.asyncio
async def test_auto_impersonate(
    devnet_forking_mode_client, impersonated_account, f_string_contract
):
    await devnet_forking_mode_client.auto_impersonate()

    contract = await Contract.from_address(
        provider=impersonated_account, address=f_string_contract.address
    )

    invocation = await contract.functions["set_string"].invoke_v1(
        "test", auto_estimate=True
    )

    await devnet_forking_mode_client.stop_auto_impersonate()

    assert invocation.invoke_transaction.sender_address == impersonated_account.address


@pytest.mark.asyncio
async def test_impersonated_account_should_fail(
    impersonated_account, f_string_contract
):
    contract = await Contract.from_address(
        provider=impersonated_account, address=f_string_contract.address
    )

    try:
        await contract.functions["set_string"].invoke_v1("test", auto_estimate=True)
        assert False
    except ClientError:
        assert True
