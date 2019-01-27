### Validation Module 
-   Each `<ValidationName>Validator.py` e,g. LinkValidator.py
- `validate()` that runs the validation against the injected markup
- `extractAccessPoints()` returns array of points E.g if is it `ImageValidator.py` then `extractAccessPoints` should return `[imgtag1, imgtag2, imgtag3]` etc. The `extractAccessPoints()`  are supposed to be used in conjunction with the `validate()` method. So, return what you would expect as input to `validate()` function
- `getResults()` returns string with \n if multiple lines 
- `isPassing()` returns boolean if all the tests are passing 
- `hasWarnings()` returns boolean if any suggested [OPTIONAL] 


### Spider Module
Spider constructor takes URL
- `getSpiderLink()` returns the link passed in URL
- `run()` hit the URL given and save it as internal member _markup for further parsing
- `getOutgoingLinks()` // returns all the tags that are outgoing 
- `getImageTags()` // returns all the tags on page with <img> 
- `getMarkup()` // returns the markup HTML

### Utility Module
- `isWithinDomain(URL, DOMAIN)` // boolean 
- `extractImageLink(imageTag)` // returns link


### Runner aka Thread Module 
Runner constructor takes these params
- `_id`- unique id for each runner auto generate GUID on object creation
- `Spider` Object
- `Validations` array
E.g. 
```
    Spider s = new Spider()
    Runner r = new Runner(s, [VALIDATIONS_TO_RUN])
```

- `Write()` results of validation in a text file based on _id. Write results inside <GUID>.txt in format
```
Link : <Link>
Validations :
    VALIDATORNAME : <RESULT>
```
E.g. 
```
Link : teachforamerica.org/teaching_offices.html
Validation:
LinkValidator : fail
Result
    http://teachforamerica.org/hunting_kids.html
ImageTags : pass
```

Example Codebase Standalone version:

```
//  create a queue 
Queue q = Queue<>; 
q.add(MAIN_URL);

// Setup results 
Writer w = new Writer('someresults.txt');

// Crawl
While( !q.isEmpty() ):
    url_to_process = q.dequeue(); // pop out URL
    
    // setup spider 
    Spider s = Spider(url_to_process)
    s.run()
    
    markup_on_page = s.Markup()
    img_tags = s.getImageTags()
    ImageValidator img = new ImageValidator();
    [] extracts = img.extractAccessPoints(markup_on_page);
    r = img.validate(extracts);
    Result r = ImageValidator(img_tags);
    
    Writer.write(r); // Writer is File IO operations handler class
    
    outgoing_links = s.getOutgoingLinks();
    
    // Look for more outgoing links
    For each link in outgoing_links: 
        If ( Util.isWithinDomain(link, MAIN_DOMAIN_URL) ) q.add(link)
```


With Runner

```
Spider s = new Spider(DOMAIN_URL);
validations = [new LinkValidator()]
Runner r = new Runner(s, validations)
r.run();
```

Inside Runner 
```
run():
    url_to_process = self.spider.getSpiderLink();
    self.spider.run()


    Writer w = new Writer(GUID.txt);

    for each validation in self.validations:
        access_points_to_validate = validation.extractAccessPoint()
        [] results = validation.validate(access_points_to_validate);
    
    w.write(results);

    for each link in spider.getOutgoingLinks():
        if (Util.isWithinDomain(link, DOMAIN)):
            Spider s = new Spider(link);
            Runner r = new Runner(Spider, validations);
            r.run(); // implement Runner as thread-able class
```
