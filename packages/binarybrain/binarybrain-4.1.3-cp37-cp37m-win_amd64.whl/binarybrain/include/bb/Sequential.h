﻿// --------------------------------------------------------------------------
//  Binary Brain  -- binary neural net framework
//
//                                     Copyright (C) 2018 by Ryuji Fuchikami
//                                     https://github.com/ryuz
//                                     ryuji.fuchikami@nifty.com
// --------------------------------------------------------------------------


#pragma once

#include <iostream>
#include <vector>
#include <memory>

#include "bb/Object.h"
#include "bb/Model.h"

namespace bb {


inline std::shared_ptr<Object> Object_Load(std::istream &is);


//! layer class
class Sequential : public Model
{
    using _super = Model;

public:
    static inline std::string ModelName(void) { return "Sequential"; }
    static inline std::string ObjectName(void){ return ModelName(); }

    std::string GetModelName(void)  const override { return ModelName(); }
    std::string GetObjectName(void) const override { return ObjectName(); }


protected:
    std::vector< std::shared_ptr<Model> > m_layers;

protected:
    Sequential() {}

public:
    /**
     * @brief  デストラクタ(仮想関数)
     * @detail デストラクタ(仮想関数)
     */
    ~Sequential() {}

    static std::shared_ptr<Sequential> Create(void)
    {
        auto self = std::shared_ptr<Sequential>(new Sequential);
        return self;
    }

    void Add(std::shared_ptr<Model> layer)
    {
        m_layers.push_back(layer);
    }

    int GetSize(void) const
    {
        return (int)m_layers.size();
    }

    std::shared_ptr<Model> Get(int index) const
    {
        return m_layers[index];
    }

    /**
     * @brief  保持するモデルリストを得る
     * @detail 保持するモデルリストを得る
     */
    std::vector< std::shared_ptr<Model> > GetList(bool flatten = true) const
    {
        std::vector< std::shared_ptr<Model> >   layers;
        for (auto model : m_layers)
        {
            auto seq = std::dynamic_pointer_cast<Sequential>(model);
            if ( flatten && seq ) {
                auto sub_layers = seq->GetList(true);
                layers.insert(layers.end(), sub_layers.begin(), sub_layers.end());
            }
            else {
                layers.push_back(model);
            }
        }
        return layers;
    }


    /**
     * @brief  コマンドを送る
     * @detail コマンドを送る
     */   
    void SendCommand(std::string command, std::string send_to = "all") override
    {
        for (auto layer : m_layers) {
            layer->SendCommand(command, send_to);
        }
    }
    
    /**
     * @brief  パラメータ取得
     * @detail パラメータを取得する
     *         Optimizerでの利用を想定
     * @return パラメータを返す
     */
    Variables GetParameters(void) override
    {
        Variables parameters;
        for (auto layer : m_layers) {
            parameters.PushBack(layer->GetParameters());
        }
        return parameters;
    }

    /**
     * @brief  勾配取得
     * @detail 勾配を取得する
     *         Optimizerでの利用を想定
     * @return パラメータを返す
     */
    virtual Variables GetGradients(void) override
    {
        Variables gradients;
        for (auto layer : m_layers) {
            gradients.PushBack(layer->GetGradients());
        }
        return gradients;
    }  

    /**
     * @brief  入力形状設定
     * @detail 入力形状を設定する
     *         内部変数を初期化し、以降、GetOutputShape()で値取得可能となることとする
     *         同一形状を指定しても内部変数は初期化されるものとする
     * @param  shape      1フレームのノードを構成するshape
     * @return 出力形状を返す
     */
    indices_t SetInputShape(indices_t shape) override
    {
        for (auto layer : m_layers) {
            shape = layer->SetInputShape(shape);
        }
        return shape;
    }

    /**
     * @brief  入力形状取得
     * @detail 入力形状を取得する
     * @return 入力形状を返す
     */
    indices_t GetInputShape(void) const override
    {
        if ( m_layers.empty() ) { return indices_t(); }
        return m_layers.front()->GetInputShape();
    }

    /**
     * @brief  出力形状取得
     * @detail 出力形状を取得する
     * @return 出力形状を返す
     */
    indices_t GetOutputShape(void) const override
    {
        if ( m_layers.empty() ) { return indices_t(); }
        return m_layers.back()->GetInputShape();
    }
    

   /**
     * @brief  forward演算
     * @detail forward演算を行う
     * @param  x     入力データ
     * @param  train 学習時にtrueを指定
     * @return forward演算結果
     */
    FrameBuffer Forward(FrameBuffer x, bool train = true) override
    {
        for (auto layer : m_layers) {
            x = layer->Forward(x, train);
        }
        return x;
    }

   /**
     * @brief  backward演算
     * @detail backward演算を行う
     *         
     * @return backward演算結果
     */
    FrameBuffer Backward(FrameBuffer dy) override
    {
        for (auto it = m_layers.rbegin(); it != m_layers.rend(); ++it) {
            dy = (*it)->Backward(dy);
        }
        return dy; 
    }
    
protected:
    /**
     * @brief  モデルの情報を表示
     * @detail モデルの情報を表示する
     * @param  os     出力ストリーム
     * @param  indent インデント文字列
     */
    void PrintInfoText(std::ostream& os, std::string indent, int columns, int nest, int depth) const override
    {
        // これ以上ネストしないなら自クラス概要
        if ( depth > 0 && (nest+1) >= depth ) {
            Model::PrintInfoText(os, indent, columns, nest, depth);
        }
        else {
            // 子レイヤーの表示
            for (auto layer : m_layers) {
                layer->PrintInfo(depth, os, columns, nest+1);
            }
        }
    }


protected:
    void DumpObjectData(std::ostream &os) const override
    {
        // バージョン
        std::int64_t ver = 2;
        SaveValue(os, ver);

        // 親クラス
        _super::DumpObjectData(os);
        
        // メンバ
        std::int64_t layer_size = (std::int64_t)m_layers.size();
        SaveValue(os, layer_size);
        for (auto& layer : m_layers) {
            layer->DumpObject(os);
        }
    }

    void LoadObjectData(std::istream &is) override
    {
        // バージョン
        std::int64_t ver;
        LoadValue(is, ver);

        BB_ASSERT(ver == 1 || ver == 2);

        if ( ver == 2 ) {
            // 親クラス
            _super::LoadObjectData(is);
        }

        // メンバ
        std::int64_t layer_size;
        LoadValue(is, layer_size);

#ifdef BB_OBJECT_LOADER
        if ( m_layers.empty() ) {
            for (std::int64_t i = 0; i < layer_size; ++i) {
                auto layer = std::dynamic_pointer_cast<Model>(Object_Load(is));
                BB_ASSERT(layer);
                m_layers.push_back(layer);
            }
            return;
        }
#endif

        BB_ASSERT(layer_size == (std::int64_t)m_layers.size());
        for (auto& layer : m_layers) {
            layer->LoadObject(is);
        }
    }


public:
    // Serialize
    void Save(std::ostream &os) const
    {
        for (auto layer : m_layers) {
            layer->Save(os);
        }
    }

    void Load(std::istream &is)
    {
        for (auto layer : m_layers) {
            layer->Load(is);
        }
    }

#if BB_WITH_CEREAL
    void Save(cereal::JSONOutputArchive& archive) const
    {
        for (auto layer : m_layers) {
            layer->Save(archive);
        }
    }

    void Load(cereal::JSONInputArchive& archive)
    {
        for (auto layer : m_layers) {
            layer->Load(archive);
        }
    }
#endif
};

}


#include "bb/ObjectLoader.h"


// end of file
