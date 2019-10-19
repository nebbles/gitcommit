from .gitcommit import main

try:
    main()
except KeyboardInterrupt:
    print("\nAborted.")
