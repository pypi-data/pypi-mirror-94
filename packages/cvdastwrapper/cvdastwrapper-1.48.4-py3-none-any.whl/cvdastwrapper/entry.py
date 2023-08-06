def main():
    import sys
    import fuzzallspecs
    import runall
    
    print(sys.argv)
    if sys.argv[1:]:
        for _ in sys.argv[1:]:
            if "--generate-tests" in _:
                fuzzallspecs.main()
            elif "--execute-tests" in _:
                runall.main()
        return