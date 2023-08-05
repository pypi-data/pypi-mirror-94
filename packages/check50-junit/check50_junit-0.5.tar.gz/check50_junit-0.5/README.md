# check50_junit

This is an extension for the [CS50 automarker check50][check50]
for compiling and running [Junit5][junit] unit tests
and raising the resulting failures directly as check50 Failures to be used in checks.

This module ships with [Junit5's stand-alone console launcher][jcl].

Your problem set only needs to include the compiled bytecode of junit test classes,
which are compiled against your model solution to the exercise.
This gets around the issue that unit tests may not compile for student's code
due to unexpected method signatures class identifiers.
Such errors will be reflected in the JUnit's report XML file.


## Example Usage

TLDR: import `check50_junit`; add your compiled junit test classes to your pset, and use `check50_junit5.run_and_interpret_test` within your checks.
A full example follows.

All examples below assume that you're importing `check50` and `check50_junit`.

1. Write your model solution and unit test classes and manually compile them.

    ```java
    public class Drink {
        private final int volume;

        public Drink(int v) {
            volume = v;
        }

        int getVolume() {
            return volume;
        }
    ```

    ```java
    import static org.junit.jupiter.api.Assertions.*;
    import org.junit.jupiter.api.Test;

    class DrinkTest {
      @Test
      public void getVolume() {
        Drink d = new Drink(200);
        assertEquals(200, d.getVolume());
      }
    }
    ```

2.  Move the bytecode `DrinkTest.class` somewhere into your pset directory, say under `tests/`.
3.  Add a check as follows (I would usually have this depend on class exists, compiles, and can be instantiated checks).
    ```python
    @check50.check()
    def drink_getVolume():
        """Test Drink.getVolume()"""
        check50_junit.run_and_interpret_test(
            classpaths=['tests/'],
            args=['--select-method', 'DrinkTest#getVolume'])
    ```
    This will run the precompiled unit test on the student submission, parse junit's XML report and raise any `check50.Failure`s as appropriate for the result. In this case it would raise a `check50.Mismatch` exception if the `assertEquals` within the unit test is thrown.

4. Make sure to add `check50-java` as a dependency in your pset's `.cs50.yml`:
    ```yml
    check50:
      dependencies:
        - check50-java
      files:
        - !exclude "*"
        - !include "*.java"
    ```



[check50]: https://github.com/cs50/check50
[run]: https://cs50.readthedocs.io/projects/check50/en/latest/api/#check50.run
[junit]: https://junit.org/junit5
[jcl]: https://junit.org/junit5/docs/current/user-guide/#running-tests-console-launcher
