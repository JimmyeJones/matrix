import streamlit as st
from fractions import Fraction
import sympy as sp
def get_num(id, st_val):
    try:
        inp = st_val.text_input("", value=0, key=id)
        if "/" in inp:
            num, den = inp.split("/")
            num = int(num)
            den = int(den)
            if den < 0 and num < 0:
                num = abs(num)
                den = abs(den)
            return num/den
        elif "." in inp:
            return float(inp)
        elif inp == "":
            return 0
        else:
            return float(inp)
    except ValueError:
        st.error("Invalid input! Please enter a number or a fraction.")
        return 0
def simp_frac(nums, D):
    ret = []
    D_frac = Fraction(D).limit_denominator()
    
    for coordinate in nums:
        coord_frac = Fraction(coordinate).limit_denominator()
        result = coord_frac / D_frac
        
        if result.denominator == 1:
            ret.append(str(int(result)))
        else:
            ret.append(str(result))
    
    return ret

st.title("Matrix Solver (Cramer's Method)")
type = st.selectbox("Matrix Size", ["2x2", "3x3"])
if type == "2x2":
    container=st.container(border=True)
    
    e = {}
    for gg in range(1,3):
        col1, i1, col2, i2, col3 = container.columns(5)
        x1 = get_num(f"x1{gg}", col1)
        i1.markdown("")
        i1.subheader("  X + ")
        y1 = get_num(f"y1{gg}", col2)
        i2.markdown("")
        i2.subheader("  Y = ")
        sol1 = get_num(f"sol{gg}", col3)
        e[f"a{gg}1"] = x1
        e[f"a{gg}2"] = y1
        e[f"s{gg}"] = sol1
    if st.button("Calculate"):
        D = (e["a11"] * e["a22"])-(e["a21"] * e["a12"])
        Dx = (e["s1"] * e["a22"])-(e["s2"] * e["a12"])
        Dy = (e["a11"] * e["s2"])-(e["a21"] * e["s1"])
            
        if D == 0:
            if Dx == 0 and Dy == 0:
                st.info("This Matrix has infinite solutions!")
                st.success("(IR, IR)")
            else:
                st.error("No Solution")
        else:
            Dx, Dy = simp_frac([Dx, Dy], D)
            st.success(f"({Dx}, {Dy})")
    
elif type == "3x3":
    container=st.container(border=True)
    col1, i1, col2, i2, col3, i3, col4 = container.columns(7)
    e = {}
    for gg in range(1,4):
        col1, i1, col2, i2, col3, i3, col4 = container.columns(7)
        x1 = get_num(f"x1{gg}", col1)
        i1.markdown("")
        i1.subheader("  X + ")
        y1 = get_num(f"y1{gg}", col2)
        i2.markdown("")
        i2.subheader("  Y + ")
        z1 = get_num(f"z1{gg}", col3)
        i3.markdown("")
        i3.subheader("  Z = ")
        sol1 = get_num(f"sol{gg}", col4)
        e[f"a{gg}1"] = x1
        e[f"a{gg}2"] = y1
        e[f"a{gg}3"] = z1
        e[f"s{gg}"] = sol1
    if st.button("Calculate"):
        D = (e["a11"] * ((e["a22"] * e["a33"])-(e["a32"] * e["a23"]))) - (e["a12"] * ((e["a21"] * e["a33"])-(e["a31"] * e["a23"]))) + (e["a13"] * ((e["a21"] * e["a32"])-(e["a31"] * e["a22"])))
        Dx = (e["s1"] * ((e["a22"] * e["a33"])-(e["a32"] * e["a23"]))) - (e["a12"] * ((e["s2"] * e["a33"])-(e["s3"] * e["a23"]))) + (e["a13"] * ((e["s2"] * e["a32"])-(e["s3"] * e["a22"])))
        Dy = (e["a11"] * ((e["s2"] * e["a33"])-(e["s3"] * e["a23"]))) - (e["s1"] * ((e["a21"] * e["a33"])-(e["a31"] * e["a23"]))) + (e["a13"] * ((e["a21"] * e["s3"])-(e["a31"] * e["s2"])))
        Dz = (e["a11"] * ((e["a22"] * e["s3"])-(e["a32"] * e["s2"]))) - (e["a12"] * ((e["a21"] * e["s3"])-(e["a31"] * e["s2"]))) + (e["s1"] * ((e["a21"] * e["a32"])-(e["a31"] * e["a22"])))
        
        if Dx == 0 and Dy == 0 and Dz == 0 and D == 0:
            st.info("This Matrix has infinite solutions!")
            C = sp.Matrix([[e["a11"], e["a12"], e["a13"]], [e["a21"], e["a22"], e["a23"]], [e["a31"], e["a32"], e["a33"]]])
            S = sp.Matrix([e["s1"], e["s2"], e["s3"]])
            x, y, z = sp.symbols('x y z')
            st.success(f"{sp.linsolve((C, S), (x, y, z)).args[0]}")
        elif D == 0:
            st.error("No Solution")
        else:
            Dx, Dy, Dz = simp_frac([Dx, Dy, Dz], D)
                        
            st.success(f"({Dx}, {Dy}, {Dz})")
