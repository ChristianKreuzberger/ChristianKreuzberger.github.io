---
title: "Make clocks great again – writing a self-contained ticking clock in Angular"
alias: "make-clocks-great-again-writing-a-self-contained-ticking-clock-in-angular"
tags:
  - "AngularJS"
  - "Informatics"
  - "Performance"
weight: 0
created_at: "2017-02-23T00:00:00Z"
updated_at: "2017-02-23T00:00:00Z"
---

During my recent journeys I discovered AngularJS, a JavaScript framework dedicated for writing Single Page Applications (SPA). One of the key concepts of Angular is the so called digest cycle. Everytime a user clicks a button, a timer caused by $timeout or $interval is fired, a $http request finishes or a $promise is resolved (or $q.defer is resolved), a digest cycle is executed.

This digest cycles causes the whole page to re-evaluate. All watchers would automatically check whether or not the variable (or function) they are watching have changed (in fact, this check is executed twice).

Now in some of my AngularJS Projects I had to implement a ticking clock, showing Hours, Minutes and Seconds. The most trivial way implementing this in Angular would be something like this:

```
$scope.updateClock = function() {
    $scope.curDate = new Date();
}
$interval($scope.updateClock, 1000); // update once per second
```

```
<p>{{ $scope.curDate | date:'hh:mm:ss' }}</p>
```

These lines of code are probably found in many AngularJS projects across the world. But what if I told you that this is in fact not a good solution? Here is why: $interval will cause a digest cycle! In this very simple example, it will cause one digest cycle per second. If you have some complex computation or many watchers, this could significantly slow down your SPA and lead to users abandoning your page. In addition, mobile devices will drain their battery much faster. The main question however is: Why would you want your whole application to evaluate again, when you only want to refresh time on your clock?

To fix this problem, we can help ourselfs by working  the concepts that JavaScript and HTML5 provide, and therefore make clocks  great again! To overcome the issue of causing unnecessary digest cycles we need to avoid using the concept of watchers and data binding of AngularJS. The experienced AngularJS programmer will already know what is coming next...

**Make DOM manipulation great again**

But but but... You aren't supposed to do that in Angular!

Right! You aren't supposed to do that in your **controllers**. However, you are allowed to do that in **directives**. Essentially, I am going to show you how to build an Angular directive which uses JavaScripts own setInterval (Note: You could use $interval and invokeApply=false) to modify a DOM element, displaying the current time.

```
    angular.module('angular-ticking-clock', []).directive('tickingClock', ['$filter', function($filter) {
        return {
            restrict: 'E',
            link: function(scope, element, attrs) {
                var updateTimer = undefined;

                var updateDateTime = function() {
                    element.text($filter('date')(new Date(), attrs.dateTimeFormat));
                };
                
                updateTimer = setInterval(updateDateTime, attrs.updateInterval);
      
                /**
                 * On Destroy of this directive, we need to cancel the timer
                */
                scope.$on(
                    "$destroy",
                    function( event ) {
                        if (updateTimer)
                            clearInterval(updateTimer);
                    }
                );

            }
        };
    }]);
```

The most important part of this is the $scope.$on("$destroy", ...)! Whenever this directive is destroyed, we need to clear the interval timer, such that it no longer fires. The second most important part is that this directive should always be used as an element (restrict: 'E'), ensuring that it has its very own DOM element to modify.

Other than that, that's it. Feel free to use this code as you like. I also created a [github Repo](https://github.com/ChristianKreuzberger/angular-ticking-clock) and an NPM package for it.