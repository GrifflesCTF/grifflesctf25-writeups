#include <iostream>
#include <cmath>

#include <fstream>
#include <sstream>
#include <vector>
#include <string>

int seen[20 + 1][570 + 1][19370 + 1] = {};
// 0 uninitialised, -1 false, 1 true

bool check_squared_sum(int size, int sum, int squared_sum)
{
    if (sum == 0 && squared_sum == 0)
        return true;
    if (size == 0)
        return false;
    if (seen[size][sum][squared_sum] != 0)
        return seen[size][sum][squared_sum] == 1;

    for (int i = floor(sqrt(squared_sum)); i > 0; --i)
    {
        if (check_squared_sum(size - 1, sum - i, squared_sum - pow(i, 2)))
        {
            seen[size][sum][squared_sum] = 1;
            return true;
        }
    }
    seen[size][sum][squared_sum] = -1;
    return false;
}

bool check(int size, double mean, double variance)
{
    double sum = size * mean;
    if (sum != round(sum))
        return false;
    int squared_sum = round(size * (variance + pow(mean, 2)));
    return check_squared_sum(size, sum, squared_sum);
}

struct CSVRow
{
    int column1;
    double column2;
    double column3;
};

std::vector<CSVRow> readCSV(std::string filename)
{
    std::vector<CSVRow> rows;
    std::ifstream file(filename);
    std::string line;

    // skip header row
    std::getline(file, line);

    while (std::getline(file, line))
    {
        std::stringstream ss(line);
        std::string item;
        CSVRow row;

        if (std::getline(ss, item, ','))
            row.column1 = std::stoi(item);
        if (std::getline(ss, item, ','))
            row.column2 = std::stod(item);
        if (std::getline(ss, item))
            row.column3 = std::stod(item);

        rows.push_back(row);
    }

    file.close();
    return rows;
}

int main()
{
    std::vector<CSVRow> data = readCSV("dataset.csv");

    for (auto &row : data)
        if (!check(row.column1, row.column2, row.column3))
            std::cout << row.column1 << ' ' << ' ' << row.column2 << ' ' << row.column3 << '\n';
}