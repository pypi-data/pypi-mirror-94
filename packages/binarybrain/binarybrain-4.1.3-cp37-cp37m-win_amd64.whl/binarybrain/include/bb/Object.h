// --------------------------------------------------------------------------
//  Binary Brain  -- binary neural net framework
//
//                                Copyright (C) 2018-2021 by Ryuji Fuchikami
//                                https://github.com/ryuz
//                                ryuji.fuchikami@nifty.com
// --------------------------------------------------------------------------


#pragma once

#include <iostream>
#include <fstream>
#include <memory>
#include <string>
#include <array>
#include <map>


#include "bb/Assert.h"


namespace bb {


class Object;
inline std::shared_ptr<Object> Object_Load(std::istream &is);


class Object
{
    friend inline std::shared_ptr<Object> Object_Load(std::istream &is);

public:
    Object(){}
    virtual ~Object() {}

    virtual std::string GetObjectName(void) const = 0;

    void DumpObject(std::ostream& os) const
    {
        WriteHeader(os, GetObjectName());
        DumpObjectData(os);
    }

    void LoadObject(std::istream& is)
    {
        auto object_name = ReadHeader(is);
        if (object_name != GetObjectName()) {
            std::cerr << "read:" << object_name << std::endl;
            std::cerr << "expect:" << GetObjectName() << std::endl;
        }

        BB_ASSERT(object_name == GetObjectName());
        LoadObjectData(is);
    }

    bool DumpToFile(std::string filename) const
    {
        std::ofstream ofs(filename, std::ios::binary);
        if ( !ofs.is_open() ) { return false; }
        DumpObject(ofs);
        return true;
    }

    bool LoadFromFile(std::string filename)
    {
        std::ifstream ifs(filename, std::ios::binary);
        if ( !ifs.is_open() ) { return false; }
        LoadObject(ifs);
        return true;
    }


#ifdef BB_PYBIND11
    pybind11::bytes DumpObjectBytes(void) const
    {
        std::ostringstream os(std::istringstream::binary);
        DumpObject(os);
        auto str = os.str();
        pybind11::bytes data(str);
        return data;
    }

    std::size_t LoadObjectBytes(pybind11::bytes data)
    {
        std::istringstream is((std::string)data, std::istringstream::binary);
        LoadObject(is);
        return (std::size_t)is.tellg();
    }

    static pybind11::bytes WriteHeaderPy(std::string name)
    {
        std::ostringstream os(std::istringstream::binary);
        WriteHeader(os, name);
        auto str = os.str();
        pybind11::bytes data(str);
        return data;
    }

    static pybind11::tuple ReadHeaderPy(pybind11::bytes data)
    {
        std::istringstream is((std::string)data, std::istringstream::binary);
        auto name = ReadHeader(is);
        return pybind11::make_tuple((std::size_t)is.tellg(), name);
    }


    pybind11::bytes DumpObjectDataBytes(void) const
    {
        std::ostringstream os(std::istringstream::binary);
        DumpObjectData(os);
        auto str = os.str();
        pybind11::bytes data(str);
        return data;
    }

    std::size_t LoadObjectDataBytes(pybind11::bytes data)
    {
        std::istringstream is((std::string)data, std::istringstream::binary);
        LoadObjectData(is);
        return (std::size_t)is.tellg();
    }
#endif


protected:
    virtual void DumpObjectData(std::ostream &os) const
    {
        // override ����Ă��Ȃ��ꍇ�� ver=0 �Ń}�[�N����(����0�ȊO�ŕ��򂷂�Βǉ��ł���)
        std::int64_t ver = 0;
        os.write((char const *)&ver, sizeof(ver));
    }
    
    virtual void LoadObjectData(std::istream &is)
    {
        // override ����Ă��Ȃ��ꍇ�͏�� 0 �����҂���
        std::int64_t ver;
        is.read((char *)&ver, sizeof(ver));
        BB_ASSERT(ver == 0);
    }


private:
    static void WriteHeader(std::ostream &os, std::string const &name)
    {
        // �^�O
        os.write("BB_OBJ", 6);
        
        // �o�[�W����
        std::int64_t ver = 1;
        os.write((char const *)&ver, sizeof(ver));

        // �I�u�W�F�N�g��
        std::uint64_t size = (std::uint64_t)name.size();
        os.write((char const *)&size, sizeof(size));
        os.write((char const *)&name[0], size*sizeof(name[0]));
    }

    static std::string ReadHeader(std::istream &is)
    {
        // �^�O
        char tag[6];
        is.read(&tag[0], 6);
        BB_ASSERT(tag[0] == 'B' && tag[1] == 'B' && tag[2] == '_' && tag[3] == 'O' && tag[4] == 'B' && tag[5] == 'J');

        // �o�[�W����
        std::int64_t ver;
        is.read((char*)&ver, sizeof(ver));
        
        // �I�u�W�F�N�g��
        std::uint64_t size;
        is.read((char *)&size, sizeof(size));
        std::string name;
        name.resize((size_t)size);
        is.read((char *)&name[0], size*sizeof(name[0]));

        return name;
    }
};


}


// end of file

