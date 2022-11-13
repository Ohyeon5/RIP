# RIP (Reveal Impacts of eco-friendly Policies)
Try this out! https://ohyeon5-rip-app-ad51gz.streamlit.app/
![Alt text](figs/default_img.png?raw=true)

## Description

### Who we are?

We're a team of three around the world whom are from three different timezones tackling climate change issues as a team participating in the OpenAI Hackathon for Climate Change.


### What we're focusing on?

We hear from so many individuals and companies about eco-friendly solutions or products being promoted, but in the second layer those solutions might be causing more CO2 emissions. Using language understanding and summarization we will attempt to understand both government and business solutions, and make outcomes of approaches to the climate crisis accessible to anyone.


### What stages are we planning to have to get results? And how are they aligned with OpenAI features?

* Finding resources we can use as an input for our solution. (GPT3 Compare for semantic search and recommendations)
* Grouping, filtering and transforming the inputs which migh be useful for our search on second layer affects of policies and applications. (GPT3 Edit)
* Generating quotes and new short definitions from what we found, as a list of takeaways. (GPT3 Explain and Write)
* Supporting our findings with auto generated images from the copies we generated. (DALL-E)


### Some resources we looked into to define the scope and context better for our model.

* https://www.ipcc.ch/reports
* https://www.iea.org/topics/world-energy-outlook
* https://www.worldbank.org/en/programs/the-world-bank-group-at-cop/publications
* https://www.consilium.europa.eu/en/policies/climate-change
* https://www.un.org/en/climatechange/science/causes-effects-climate-change
* https://climate-laws.org



## Getting Started

### Dependencies

* TODO: Describe any prerequisites, libraries, OS version, etc., needed before installing program.

### Installing

* Add API_KEY to use openAI APIs

    * Add `api_secrets.py` in the root directory and save your openAI API key as a variable
    ```    
    import os

    ORGANIZATION='org-...'
    API_KEY='sk-...'

    #override if there's a key defined as a system wide parameter
    if os.getenv('OPENAI_ORG') != None:
        ORGANIZATION=os.getenv('OPENAI_ORG')
        
    if os.getenv('OPENAI_API_KEY') != None:
        API_KEY=os.getenv('OPENAI_API_KEY')
    ```

### Executing program

* Test with any scripts in `./examples` to check if it works (optional)
* From root path, run: 
```
(Linux or Mac users)> sh ./scripts/start-streamlit-app-linux
(Windows users)     > ./scripts/start-streamlit-app-windows.bat
```


## Help

TODO: Any advise for common problems or issues.


## Authors

Contributors names and contact info

* Metin Aydar [@metinaydar](https://github.com/metinaydar)
* Leif Martinson [@lfhvn](https://github.com/lfhvn)
* Oh-hyeon Choung [@Ohyeon5](https://github.com/Ohyeon5)


## Version History

* 0.3
    * Updates on the README for more descriptive context
* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release


## License

This project is licensed under the MIT License - see the LICENSE.md file for details


## Acknowledgments
TODO: Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b
