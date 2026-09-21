CXX := g++
AR := ar
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -O2
CPPFLAGS := -I.

BUILD_DIR := .make-build
TARGET := $(BUILD_DIR)/calc_app
LIBRARY := $(BUILD_DIR)/libcalculator.a
OBJECTS := $(BUILD_DIR)/main.o $(BUILD_DIR)/calculator.o

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(BUILD_DIR)/main.o $(LIBRARY)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(LIBRARY): $(BUILD_DIR)/calculator.o
	$(AR) rcs $@ $^

$(BUILD_DIR)/%.o: %.cpp calculator.h | $(BUILD_DIR)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

$(BUILD_DIR):
	mkdir -p $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -rf $(BUILD_DIR)
