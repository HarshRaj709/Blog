                            ---> Index <--

    1   -----------------------------------------------     Commands

    2   -----------------------------------------------     Fixtures

    3   -----------------------------------------------     Parametrization of Tests

    4   -----------------------------------------------     Mocking in pytest

    5   -----------------------------------------------     Marking in pytest

    6   -----------------------------------------------     Advanced Features in Pytest

Applied on 
    blogs/tests/blog_tests.py
    authentication/tests/authentication_tests.py


Some Important Commands

    -> pytest : to run all commands
    -> pytest -s: to see all print statements within testcases
    -> pytest -rp: to see short summary of all tests
    -> pytest --fixtures: to see all fixtures
    -> pytest --fixtures -v: More cleared fixture info
    -> pytest --maxfail 2: then test get stops if 2 testcases fails
    -> pytest -m <marker name>: to run only marked tests pytest -m slow
    -> pytest -v : it gives detailed verbose of output rather than just .


---------------------------------------------------------------------------------------

-> Fixture runs everytime a function runs. It helps to provide necessary data to the     function
-> Reduce code duplicacy
-> it has 2 parts which we can seperate by using "yield" keywords.
-> Everything above yield will run before the functions
-> And Everything after yield will run after function
-> Like if there are 4 testcases then it will run 4 times.


---------------------------------------------------------------------------------------

                            Fixtures And there Scope

Mainly there are 4 scopes available in Fixtures.

1.Function
2.Module
3.Class
4.Session

Function : Default

import pytest

# This fixture will be run for every test function that uses it.
@pytest.fixture(scope="function")           or  @pytest.fixture
def function_fixture():
    print("\n[Function Setup]")
    yield
    print("[Function Teardown]")

def test_one(function_fixture):
    print("Running test_one")
    assert True

def test_two(function_fixture):
    print("Running test_two")
    assert True

                                output
            [Function Setup]
            Running test_one
            .[Function Teardown]

            [Function Setup]
            Running test_two
            .[Function Teardown]

---------------------> Module Scope

What it means: The fixture is executed once per module (i.e., per file) regardless of 
                how many tests in that file use it.

When to use: When you have a setup that can be shared across multiple tests in the 
                same file.


    @pytest.fixture(scope="module")
    def fixture():
        print('running at starting')
        yield
        print('Ending of the fixtures')

    def test_first(fixture):
        print('executing 1st test')
        assert True

    def test_sec(fixture):
        print('executing 2nd test')
        assert True


                                    Output
        
    running at starting
    executing 1st test
    .executing 2nd test
    .Ending of the fixtures

-------------------> Class Scope

What it means: The fixture is executed once per class that contains tests 
                (typically used when tests are methods of a class).

When to use: When all tests within a class can share the same setup.


    
    import pytest

    # This fixture will be set up once for all test methods in the class.
    @pytest.fixture(scope="class")
    def class_fixture():
        print("\n[Class Setup]")
        yield
        print("[Class Teardown]")

    class TestExample:
        
        def test_first(self, class_fixture):
            print("Running test_first")
            assert True

        def test_second(self, class_fixture):
            print("Running test_second")
            assert True



                                    Output

    [Class Setup]
    Executing 1st
    .Executing 2nd
    .[Class Teardown]


------------------------> session Scope

What it means: The fixture is executed once per entire test session (
                i.e., across all test files).

When to use: For expensive setups (like connecting to a database or starting a server)
                 that you only want to do one time for the whole test run.
        

        # This fixture will be set up once for the entire session.
        @pytest.fixture(scope="session")
        def fixture():
            print("\n[Session Setup]")
            yield
            print("[Session Teardown]")


        def test_first(fixture):
            print('Executing 1st')
            assert True

        def test_sec(fixture):
            print('Executing 2nd')
            assert True


Thats all about Fixture scopes..

--------------------------------------------------------------------------------------

                                Fixture Autouse
Normally, to use a fixture in a test, you must include it as a parameter in your test 
function. However, sometimes you want a fixture to run automatically for every test 
without explicitly adding it. That’s where autouse comes in.

What it means: When a fixture is defined with autouse=True, pytest will automatically 
apply it to tests in its scope, even if you don’t mention it as a parameter.
When to use: When you need some setup/teardown logic to run for every test without 
extra boilerplate in each test function.


                                Without autouse
        import pytest

        @pytest.fixture
        def manual_fixture():
            print("\n[Manual Fixture Setup]")
            yield
            print("[Manual Fixture Teardown]")

        def test_manual(manual_fixture):
            print("Running test_manual")
            assert True


                            With AutoUse

        @pytest.fixture(autouse=True)
        def auto_fixture():
            print("\n[Autouse Fixture Setup]")
            yield
            print("[Autouse Fixture Teardown]")

        def test_auto_one():
            print("Running test_auto_one")
            assert True

        def test_auto_two():
            print("Running test_auto_two")
            assert True



---------------------------------------------------------------------------------------

                    Parametrization of Tests in pytest
In pytest, you can easily run the same test function with different sets of data using parametrization. This helps you avoid writing repetitive test code and allows you to check different scenarios or edge cases by passing different input values to your tests.



The main way to do this is with the **`@pytest.mark.parametrize`** decorator.

### **1. Parameterized Tests with `@pytest.mark.parametrize`**

- **What it means:** The `@pytest.mark.parametrize` decorator allows you to run the same test multiple times with different sets of arguments (data). This is useful when you want to test a function or feature with a variety of inputs without writing separate test functions for each case.

                                 **Syntax:**

@pytest.mark.parametrize("argument1, argument2", [(value1, value2), (value3, value4), ...])
def test_function(argument1, argument2):
    # Your test code


- **`"argument1, argument2"`**: The names of the arguments your test function will receive.
- **`[(value1, value2), (value3, value4), ...]`**: A list of tuples, where each tuple is a set of arguments to pass to the test.

#### **Example:**


import pytest

# Using parametrize to test with different values
@pytest.mark.parametrize("x, y, expected_sum", [(1, 2, 3), (4, 5, 9), (7, 8, 15)])
def test_addition(x, y, expected_sum):
    result = x + y
    assert result == expected_sum


**What happens:**
- The `test_addition` function will run three times:
  - Once with `x=1`, `y=2`, and `expected_sum=3`
  - Once with `x=4`, `y=5`, and `expected_sum=9`
  - Once with `x=7`, `y=8`, and `expected_sum=15`
  
- For each run, it will check if the sum of `x` and `y` matches the `expected_sum`.

                                #### **Output:**

test_addition.py::test_addition[1-2-3] PASSED
test_addition.py::test_addition[4-5-9] PASSED
test_addition.py::test_addition[7-8-15] PASSED


This approach helps you test the same logic with multiple data points, ensuring your function behaves as expected in various scenarios.

---------------------------------------------------------------------------------------

                    2. Using Parametrization for Input-Output Pairs

Sometimes, you want to test a function that takes an input and returns an output, and you want to check several input-output pairs. You can easily do this with parameterized tests.

#### **Example:**

Let’s say you have a function `multiply` that takes two numbers and returns their product. You want to test it with different pairs of inputs and their expected outputs.


import pytest

# Function to test
def multiply(a, b):
    return a * b

# Using parametrize for input-output pairs
@pytest.mark.parametrize("a, b, expected_result", [(2, 3, 6), (5, 4, 20), (10, -2, -20), (0, 7, 0)])
def test_multiply(a, b, expected_result):
    assert multiply(a, b) == expected_result


**What happens:**
- The `test_multiply` function will run four times:
  - Once with `a=2`, `b=3`, and `expected_result=6`
  - Once with `a=5`, `b=4`, and `expected_result=20`
  - Once with `a=10`, `b=-2`, and `expected_result=-20`
  - Once with `a=0`, `b=7`, and `expected_result=0`

- For each test case, it will check whether the product of `a` and `b` matches the `expected_result`.

                                #### **Output:**

test_multiply.py::test_multiply[2-3-6] PASSED
test_multiply.py::test_multiply[5-4-20] PASSED
test_multiply.py::test_multiply[10--2--20] PASSED
test_multiply.py::test_multiply[0-7-0] PASSED


This way, you can easily run tests on multiple sets of input-output pairs without writing separate test functions for each case.

---------------------------------------------------------------------------------------

                    **3. Advanced Example: Testing Edge Cases**

Parametrization can also be used to test edge cases, such as when the inputs are at their minimum, maximum, or other unusual values.

For example, let’s say you want to test the `divide` function with different pairs of inputs, including edge cases like dividing by zero.

#### **Example:**


import pytest

# Function to test
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Testing edge cases with parametrize
@pytest.mark.parametrize("a, b, expected_result", [
    (10, 2, 5),       # normal case
    (20, 4, 5),       # normal case
    (10, 0, ValueError)  # edge case: division by zero
])
def test_divide(a, b, expected_result):
    if expected_result == ValueError:
        with pytest.raises(ValueError):
            divide(a, b)
    else:
        assert divide(a, b) == expected_result


                                **What happens:**

- The `test_divide` function will run three times:
  - Once with `a=10`, `b=2`, and `expected_result=5`
  - Once with `a=20`, `b=4`, and `expected_result=5`
  - Once with `a=10`, `b=0`, and it expects a `ValueError` because dividing by zero is not allowed.

                                #### **Output:**

test_divide.py::test_divide[10-2-5] PASSED
test_divide.py::test_divide[20-4-5] PASSED
test_divide.py::test_divide[10-0-ValueError] PASSED


This example tests a function that handles division and raises an exception when dividing by zero, covering both typical and edge cases.

---------------------------------------------------------------------------------------

                            Mocking and Patching in Pytest 

What is Mocking?

- Mocking means **replacing a real object (function, class, or API call) with a fake one (mock object)** in your tests.
- This helps you **isolate the part of the code being tested**, avoiding external dependencies like databases, APIs, or complex calculations.

- Mocking is useful when:
  - Your function calls a **third-party API** (e.g., fetching weather data).
  - Your function interacts with a **database**.
  - Your function depends on **other parts of your app** that are not relevant to the test.

Why Use Mocking?
- Faster Tests → Avoids slow network calls or database queries.
- Independent Testing → Tests only the function logic, not external systems.
- Avoid Unreliable Factors → No failures due to API downtime or database issues.

---------------------------------------------------------------------------------------

2. Using `unittest.mock` with Pytest**
Python provides a built-in library called `unittest.mock` for mocking. It has two main tools:
1. `Mock()` → Creates a fake object.
2. `patch()` → Temporarily replaces an object with a mock.

2.1 Mocking a Function Call
Let’s say you have a function that fetches user data from an API.

                    Code Without Mocking (Slow & Dependent on API)**

import requests

def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

                        Test Without Mocking (Not Recommended)

def test_get_user_data():
    data = get_user_data(1)
    assert "name" in data  # Test will fail if API is down


---------------------------------------------------------------------------------------

2.2 Mocking the API Call (Recommended)
We use `patch()` to replace `requests.get` with a **mocked function** that returns **fake data**.


from unittest.mock import patch

def test_get_user_data():
    fake_response = {"id": 1, "name": "Alice"}  # Fake API response
    
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_response  # Mock API response
        data = get_user_data(1)

    assert data == fake_response  # ✅ Passes even if API is down


How it works:  
- `patch("requests.get")` replaces `requests.get` with a **mock function**.
- `mock_get.return_value.json.return_value = fake_response` makes it return **fake data.


---------------------------------------------------------------------------------------

3. Using `patch()` as a Decorator
Instead of using `with patch(...)`, you can use a **decorator** for cleaner code.

Example:

@patch("requests.get")
def test_get_user_data(mock_get):
    fake_response = {"id": 1, "name": "Alice"}
    mock_get.return_value.json.return_value = fake_response  # Mock API response

    data = get_user_data(1)
    
    assert data == fake_response  # ✅ Passes


🔹 **Key Benefits:**  
✔️ **Cleaner Code** → No need for `with patch(...)`.  
✔️ **Same Functionality** → `mock_get` is automatically injected.

---------------------------------------------------------------------------------------

4. Mocking a Class Method
Let’s say we have a **UserService** class that fetches user data.


class UserService:
    def get_user_name(self, user_id):
        response = requests.get(f"https://api.example.com/users/{user_id}")
        return response.json().get("name")


                        Test Without Mocking (API Dependent)

def test_get_user_name():
    service = UserService()
    name = service.get_user_name(1)  
    assert name is not None  # ❌ Fails if API is down


                        Test With Mocking (Independent)

@patch("requests.get")
def test_get_user_name(mock_get):
    fake_response = {"id": 1, "name": "Alice"}
    mock_get.return_value.json.return_value = fake_response  # Mock API response

    service = UserService()
    name = service.get_user_name(1)

    assert name == "Alice"  # ✅ Passes even without API


---------------------------------------------------------------------------------------

5. Mocking a Database Call
Let’s say we have a function that fetches a user’s email from a database.


class Database:
    def get_email(self, user_id):
        # Imagine this is a real database query
        return "user@example.com"


                    Test Without Mocking (Slow & Requires Database)

def test_get_email():
    db = Database()
    email = db.get_email(1)
    assert email == "user@example.com"


                        Test With Mocking (Fast & Independent)

from unittest.mock import MagicMock

def test_get_email():
    db = Database()
    db.get_email = MagicMock(return_value="mock@example.com")  # Mock the method
    
    email = db.get_email(1)
    
    assert email == "mock@example.com"  # ✅ Passes without a real database


---------------------------------------------------------------------------------------

6. Mocking Time-Related Functions
Let’s say your function depends on the current time.


import time

def get_current_timestamp():
    return time.time()

                      Test Without Mocking (Unpredictable)

def test_get_current_timestamp():
    assert get_current_timestamp() < 9999999999  # ❌ Fails unpredictably


                        Test With Mocking (Stable)

@patch("time.time", return_value=1623456789)  # Fake timestamp
def test_get_current_timestamp(mock_time):
    assert get_current_timestamp() == 1623456789  # ✅ Predictable test


---------------------------------------------------------------------------------------

7. Mocking Built-in `open()` Function

If your function reads a file, you can mock `open()` to avoid real file access.


def read_file():
    with open("data.txt", "r") as file:
        return file.read()


                        Test Without Mocking (Requires File)

def test_read_file():
    assert read_file() == "Hello, World!"  # ❌ Fails if file is missing


                        Test With Mocking (Independent)

from unittest.mock import mock_open

@patch("builtins.open", new_callable=mock_open, read_data="Mock Data")
def test_read_file(mock_file):
    assert read_file() == "Mock Data"  # ✅ Works without an actual file


---------------------------------------------------------------------------------------

### ✅ **How to Use Mocking in Pytest?**
| **Scenario**               | **Solution** |
|----------------------------|-------------|
| Mocking a function call    | `patch("module.function")` |
| Mocking a class method     | `patch("module.Class.method")` |
| Mocking database queries   | `MagicMock()` |
| Mocking time functions     | `patch("time.time", return_value=12345)` |
| Mocking file reading       | `patch("builtins.open", new_callable=mock_open, read_data="Mock Data")` |

### **Mocking = Faster, More Reliable, Easier Testing! 🚀**


---------------------------------------------------------------------------------------

                            Advanced Features in Pytest:

                        
Custom Markers:

Pytest allows us to "tag" tests using custom markers. This helps in:
✔ Running only specific tests
✔ Skipping tests when needed
✔ Categorizing tests (e.g., slow tests, database tests, etc.)

                        ✅ How to Add Custom Markers?

1️⃣ Define custom markers in pytest.ini (to avoid warnings)
2️⃣ Use @pytest.mark.<marker_name> in tests
3️⃣ Run tests using -m <marker_name>


                                    Example
[pytest]
markers =
    slow: Tests that take a long time
    api: Tests that interact with an API

                ---------------------------------------------------------
import pytest

@pytest.mark.slow
def test_big_calculation():
    """A test that takes a long time"""
    result = sum(range(1000000))
    assert result > 0

@pytest.mark.api
def test_api_response():
    """A test for an API call"""
    response = {"status": 200, "data": "Hello"}
    assert response["status"] == 200

            -------------------------------------------------------------

command :- pytest -m slow

                    2️⃣ Test Reporting – Generating HTML Reports

Pytest allows beautiful test reports in HTML format, which are useful for debugging.

🔹 Install pytest-html
    pip install pytest-html

🔹 Run Tests and Generate HTML Report
    pytest --html=report.html

This creates a file report.html, which you can open in a browser.

            ---------------------------------------------------------------


3️⃣ Test Coverage – Ensuring Code is Fully Tested

Pytest can check how much of your code is actually tested!

🔹 Install pytest-cov
    pip install pytest-cov

🔹 Run Tests with Coverage Report
    pytest --cov=my_app

This shows which lines of my_app are tested and which are not.

🔹 Generate a Detailed HTML Report
    pytest --cov=my_app --cov-report=html

Now, open htmlcov/index.html in a browser to see which lines of code are missing tests! ✅

            --------------------------------------------------------------


4️⃣ Running Tests in Parallel – Faster Testing 🚀

If you have many tests, running them one by one is slow.
The pytest-xdist plugin allows running multiple tests at the same time (parallel execution).

🔹 Install pytest-xdist
    pip install pytest-xdist

🔹 Run Tests in Parallel
    pytest -n 4  # Runs tests using 4 CPU cores

This makes testing MUCH faster, especially for large projects.

---------------------------------------------------------------------------------------

Pytest for Django (or other frameworks):
Pytest with Django:
Learn how to integrate pytest with Django to test Django views, models, forms, and API endpoints.
Using pytest-django for Django tests:
Use specific pytest features like fixtures for Django database handling and more.