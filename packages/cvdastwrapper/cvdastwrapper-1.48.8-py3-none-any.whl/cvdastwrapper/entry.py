def main():
    import sys
    from . import fuzzallspecs
    from . import runall
    
    print(sys.argv[1:], "argv")
    if sys.argv[1:]:
        if "--generate-tests" in sys.argv[1:]:
            print(sys.argv)
            fuzzallspecs.fuzzspecs()                
            return
    runall.main()            
    
        
if __name__ == "__main__":
    # execute only if run as a script
    main()
        