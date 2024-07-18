import pytest_asyncio

from starknet_py.contract import Contract
from starknet_py.tests.e2e.fixtures.contracts import deploy_v1_contract
from starknet_py.tests.e2e.fixtures.contracts_v1 import declare_cairo1_contract
from starknet_py.tests.e2e.fixtures.misc import ContractVersion, load_contract


@pytest_asyncio.fixture(scope="package", name="f_string_contract_class_hash")
async def declare_string_contract(forked_devnet_account) -> int:
    contract = load_contract("MyString", version=ContractVersion.V2)
    class_hash, _ = await declare_cairo1_contract(
        forked_devnet_account, contract["sierra"], contract["casm"]
    )
    return class_hash


@pytest_asyncio.fixture(scope="package", name="f_string_contract")
async def deploy_string_contract(
    forked_devnet_account, f_string_contract_class_hash
) -> Contract:
    return await deploy_v1_contract(
        account=forked_devnet_account,
        contract_name="MyString",
        class_hash=f_string_contract_class_hash,
    )
