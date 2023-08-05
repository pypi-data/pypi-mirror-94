import matplotlib.pyplot as plt

#making a simple plot
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

plt.plot(years, gdp, color = "green", marker = "o", linestyle = "solid")
plt.title("Nominal GDP") #title
plt.ylabel("Billions of $") #y-label
plt.show()

plt.cla()

#bar charts - useful to show how something varies amoung categories
movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
num_oscars = [5, 11, 3, 8, 10]
plt.bar(range(len(movies)), num_oscars)
plt.title("My 'fav' movies ")
plt.ylabel("# of Acadmemy awards")
plt.xticks(range(len(movies)), movies) #x-axis with the movie names at the bottom
plt.show()

    #bar charts are also good for plotting histograms of buckets - which is useful for seeing the distribution of something

plt.cla()
from collections import Counter
grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]

histogram = Counter(min(grade // 10 * 10, 90) for grade in grades)

plt.bar([x + 5 for x in histogram.keys()], #shift by 5 to the right makes sure everything is centered - otherwise the values become the centers, so 0 is the center and the range is from [-5, 5]
        histogram.values(),
        10, #give width 10
        edgecolor = (0,0,0)) #black borders

plt.axis([-5, 105, 0, 5]) #x_range = -5 to 105 ; y_range = 0 to 5 - leave space for x range so there is a buffer

plt.xticks([10 * i for i in range(11)])
plt.xlabel("Decile")
plt.ylabel("# of students")
plt.title("Distribution of grades")
plt.show()

#MISLEADING BAR CHARTS
plt.cla()

mentions = [500, 505]
years = [2017, 2018]

plt.bar(years, mentions, 0.8)
plt.xticks(years)
plt.ylabel("# of times I hear 'machine learning'")
plt.ticklabel_format(useOffset=False)

plt.axis([2016.5, 2018.5, 499, 506]) #[x_min, x_max, y_min, y_max]
plt.title("ML kinda hot rn")
plt.show()

#but if you start the y-axis @ 0
plt.axis([2016.5, 2018.5, 0, 600])
plt.title("Kinda dumb")
plt.show()

plt.cla()

#line charts can be useful to show trends

variance = [1, 2, 4, 8, 16, 32, 64, 128, 256]
bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]
total_error = [x + y for x, y in zip(variance, bias_squared)]
xs = [i for i , _ in enumerate(variance)]

    #you can make multiple plt.plots()

plt.plot(xs, variance, "g-", label = "variance") #green solid line
plt.plot(xs, bias_squared, "r-.", label = "bias^2") #dot-dash line in red
plt.plot(xs, total_error, "b:", label = "total error") #blue dotted line

plt.legend(loc = 9) #loc = 9 means top center for the ley
plt.xlabel("model complexity")
plt.xticks([])
plt.title("The Bias-Variance Tradeoff")
plt.show()

#using scatterplots to visualize relationship between two points of data
plt.cla()

friends = [70, 65, 72, 63, 71, 64, 60, 64, 67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

plt.scatter(friends, minutes)

    #you also want to label each point
for label, friend_count, minute_count in zip(labels, friends, minutes) :
    plt.annotate(
        label,
        xy = (friend_count, minute_count), #just find the point
        xytext = (5, -5),
        textcoords = "offset points"
    )

plt.title("Daily Minutes vs. Number of Friends")
plt.xlabel("# of friends")
plt.ylabel("daily minutes on the site")
plt.show()

#always make sure the scale of the data is same in the plots generated!

plt.cla()

test_1_grades = [99, 90, 85, 97, 90]
test_2_grades = [100, 85, 60, 90, 70]

plt.scatter(test_1_grades, test_2_grades)
plt.title("Axes aren't Comparable")
plt.xlabel("Test 1 grade")
plt.ylabel("Test 2 grade")
plt.show()

plt.cla()
plt.scatter(test_1_grades, test_2_grades)
plt.title("Better axises")
plt.xlabel("Test 1 grade")
plt.ylabel("Test 2 grade")
plt.axis("equal") #sets better axises
plt.show()

#this now shows much better that there is higher variance among test 2 than test 1 in the grades