from hamcrest import *
from nose.tools import istest, raises
import numpy
from cis.data_io.Coord import Coord, CoordList
from cis.data_io.ungridded_data import Metadata
from cis.exceptions import DuplicateCoordinateError


def create_dummy_coordinates_list():
    coord1 = Coord(numpy.array([5, 4]), Metadata(standard_name='grid_latitude'), axis='Y')
    coord2 = Coord(numpy.array([5, 4]), Metadata(standard_name='grid_longitude'), axis='X')
    return CoordList([coord1, coord2])


@istest
def can_create_a_valid_list_of_coordinates():
    list = create_dummy_coordinates_list()
    assert (len(list) == 2)
    assert (list[0].standard_name == 'grid_latitude')
    assert (list[1].standard_name == 'grid_longitude')
    assert (list[0].axis == 'Y')
    assert (list[1].axis == 'X')


@istest
def can_append_to_list_of_coordinates():
    list = create_dummy_coordinates_list()
    list.append(Coord(numpy.array([5, 4]), Metadata(standard_name='altitude'), axis='Z'))
    assert (len(list) == 3)
    assert (list[2].standard_name == 'altitude')
    assert (list[2].axis == 'Z')


@istest
@raises(DuplicateCoordinateError)
def append_a_duplicate_to_a_list_of_coordinates_fails():
    list = create_dummy_coordinates_list()
    list.append(Coord(numpy.array([5, 4]), Metadata(standard_name='grid_longitude'), axis='X'))


@istest
def can_find_a_coord_from_a_list_of_coordinates():
    list = create_dummy_coordinates_list()
    coord = list.get_coord(standard_name='grid_longitude')
    assert (coord.standard_name == 'grid_longitude')
    assert (coord.axis == 'X')


@istest
def can_find_many_coords_from_a_list_of_coordinates():
    list = create_dummy_coordinates_list()
    list.append(Coord(numpy.array([5, 4]), Metadata(name='testZ'), axis='Z'))
    list.append(Coord(numpy.array([5, 4]), Metadata(name='testZ', standard_name='air_pressure')))
    assert (len(list) == 4)
    coords = list.get_coords(var_name='testZ')
    assert (len(coords) == 2)
    assert (coords[0].axis == 'Z')
    assert (coords[1].axis == '')
    assert (coords[1].name() == 'air_pressure')

@istest
def can_convert_time_without_since_in_units():
    times = numpy.array([0, 1])
    units = "Days from the file reference point 1601-01-01"
    time_stamp_info = "1601-01-01"
    coord = Coord(times, Metadata(units=units))

    coord.convert_to_std_time(time_stamp_info)

    assert_that(coord.data_flattened[0], is_(366.0), "time point")


@istest
def can_convert_time_with_since_in_units():
    times = numpy.array([0, 1])
    units = "days since 1601-01-01"
    coord = Coord(times, Metadata(units=units))

    coord.convert_to_std_time()

    assert_that(coord.data_flattened[0], is_(366.0), "time point")


@istest
@raises(ValueError)
def can_not_convert_time_without_since_in_units_but_no_timestamp():
    times = numpy.array([0, 1])
    units = "Days from the file reference point 1601-01-01"
    coord = Coord(times, Metadata(units=units))

    coord.convert_to_std_time()


@istest
@raises(ValueError)
def can_not_convert_time_without_since_in_units_with_no_units():
    times = numpy.array([0, 1])
    units = ""
    time_stamp_info = "1601-01-01"
    coord = Coord(times, Metadata(units=units))

    coord.convert_to_std_time(time_stamp_info)
